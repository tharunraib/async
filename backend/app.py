import os,re,hashlib,json
from uuid import uuid4
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import psycopg
DB=os.getenv("DATABASE_URL","postgresql://rootcause:rootcause@localhost:5432/rootcause")
app=FastAPI(title="Root Cause",version="0.1.0")
def db(): return psycopg.connect(DB)
def fingerprint(text,component=None,symptom=None,dependency=None,owner=None):
    def pick(v,pat):
        if v:return v
        m=re.search(pat,text,re.I);return m.group(1) if m else None
    if not symptom:
        for x in ["timeout","connection pool","5xx","latency","oom","deadlock","authentication","rate limit","queue backlog"]:
            if x in text.lower(): symptom=x; break
    return {"component":pick(component,r"(?:component|service|module)[:= ]+([\\w.-]+)"),"symptom":symptom or "unknown","dependency":pick(dependency,r"(?:dependency|depends on|upstream)[:= ]+([\\w.-]+)"),"owner":pick(owner,r"(?:owner|team)[:= ]+([\\w.-]+)")}
def audit(kind,payload):
    c=json.dumps(payload,sort_keys=True,separators=(",",":"))
    with db() as x:
        row=x.execute("select event_hash from audit_events order by id desc limit 1").fetchone(); prev=row[0] if row else "GENESIS"
        h=hashlib.sha256((prev+c).encode()).hexdigest(); x.execute("insert into audit_events(event_type,payload,previous_hash,event_hash) values(%s,%s,%s,%s)",(kind,payload,prev,h)); return h
class Incident(BaseModel):
    external_id:str; title:str; body:str; component:str|None=None; symptom:str|None=None; dependency:str|None=None; owner:str|None=None; occurred_at:str
class Preflight(BaseModel):
    change_title:str; components:list[str]; description:str
@app.get("/health")
def health(): return {"status":"ok","service":"root-cause"}
@app.post("/api/incidents")
def ingest(i:Incident):
    f=fingerprint(i.body,i.component,i.symptom,i.dependency,i.owner); iid=uuid4()
    try:
        with db() as x:
            x.execute("insert into incidents(id,external_id,title,body,component,symptom,dependency,owner,occurred_at,valid_from) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(iid,i.external_id,i.title,i.body,f["component"],f["symptom"],f["dependency"],f["owner"],i.occurred_at,i.occurred_at))
            for chunk in [i.body[j:j+1200] for j in range(0,len(i.body),1200)]: x.execute("insert into chunks(incident_id,content) values(%s,%s)",(iid,chunk))
        audit("incident.ingested",{"incident_id":str(iid),"external_id":i.external_id}); return {"id":str(iid),"fingerprint":f}
    except Exception as e: raise HTTPException(400,str(e))
@app.get("/api/incidents")
def incidents(limit:int=50):
    with db() as x:r=x.execute("select id,external_id,title,component,symptom,dependency,owner,occurred_at from incidents order by occurred_at desc limit %s",(limit,)).fetchall()
    return [{"id":str(a),"external_id":b,"title":c,"component":d,"symptom":e,"dependency":f,"owner":g,"occurred_at":h} for a,b,c,d,e,f,g,h in r]
@app.post("/api/retrieval/search")
def search(query:str,limit:int=8):
    with db() as x:r=x.execute("select i.external_id,i.title,c.content,ts_rank(c.search_vector,plainto_tsquery('english',%s)) score from chunks c join incidents i on i.id=c.incident_id where c.search_vector @@ plainto_tsquery('english',%s) order by score desc limit %s",(query,query,limit)).fetchall()
    return [{"external_id":a,"title":b,"evidence":c,"score":float(d)} for a,b,c,d in r]
@app.post("/api/clusters/detect")
def clusters():
    with db() as x:r=x.execute("select id,component,symptom,dependency from incidents order by occurred_at").fetchall()
    groups={}
    for row in r: groups.setdefault((row[1],row[2],row[3]),[]).append(row[0])
    out=[]
    for key,members in groups.items():
        if len(members)<3: continue
        cid=uuid4(); label=" / ".join(v or "unknown" for v in key); hyp=f"Recurring failure pattern around {label}"; confidence=min(1,len(members)/5)
        with db() as x:
            x.execute("insert into recurrence_clusters(id,label,hypothesis,confidence) values(%s,%s,%s,%s)",(cid,label,hyp,confidence))
            for iid in members:x.execute("insert into cluster_members(cluster_id,incident_id) values(%s,%s) on conflict do nothing",(cid,iid))
        out.append({"cluster_id":str(cid),"label":label,"members":len(members),"confidence":confidence})
    return out
@app.post("/api/preflight")
def preflight(p:Preflight):
    with db() as x:r=x.execute("select distinct rc.id,rc.label,rc.hypothesis,rc.confidence from recurrence_clusters rc join cluster_members cm on cm.cluster_id=rc.id join incidents i on i.id=cm.incident_id where i.component=any(%s)",(p.components,)).fetchall()
    result={"warning":bool(r),"change":p.change_title,"matches":[{"cluster_id":str(a),"label":b,"hypothesis":c,"confidence":d} for a,b,c,d in r]}; audit("preflight.checked",result); return result
@app.get("/api/audit")
def audit_log(limit:int=100):
    with db() as x:r=x.execute("select id,event_type,payload,previous_hash,event_hash,created_at from audit_events order by id desc limit %s",(limit,)).fetchall()
    return [{"id":a,"event_type":b,"payload":c,"previous_hash":d,"event_hash":e,"created_at":f} for a,b,c,d,e,f in r]
