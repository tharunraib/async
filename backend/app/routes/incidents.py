from uuid import uuid4
from fastapi import APIRouter, HTTPException
from app.db import connection
from app.schemas import IncidentCreate
from app.services.fingerprint import fingerprint
from app.services.audit import append_event

router = APIRouter(tags=["incidents"])

@router.post("/incidents")
def create_incident(item: IncidentCreate):
    fp = fingerprint(item.body, item.component, item.symptom, item.dependency, item.owner)
    incident_id = uuid4()
    try:
        with connection() as conn:
            conn.execute(
                """INSERT INTO incidents(id,external_id,title,body,component,symptom,dependency,owner,occurred_at,valid_from)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (incident_id,item.external_id,item.title,item.body,fp["component"],fp["symptom"],fp["dependency"],fp["owner"],item.occurred_at,item.occurred_at),
            )
    except Exception as exc:
        raise HTTPException(400, str(exc))
    append_event("incident.ingested", {"incident_id": str(incident_id), "external_id": item.external_id})
    return {"id": str(incident_id), "fingerprint": fp}

@router.get("/incidents")
def list_incidents(limit: int = 50):
    with connection() as conn:
        rows = conn.execute("SELECT id,external_id,title,component,symptom,dependency,owner,occurred_at FROM incidents ORDER BY occurred_at DESC LIMIT %s", (limit,)).fetchall()
    return [{"id":str(r[0]),"external_id":r[1],"title":r[2],"component":r[3],"symptom":r[4],"dependency":r[5],"owner":r[6],"occurred_at":r[7]} for r in rows]
