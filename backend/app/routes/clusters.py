from uuid import uuid4
from fastapi import APIRouter
from app.db import connection
from app.services.debt import failure_debt

router = APIRouter(tags=["clusters"])

@router.post("/clusters/detect")
def detect_clusters():
    with connection() as conn:
        incidents = conn.execute("SELECT id,component,symptom,dependency FROM incidents ORDER BY occurred_at").fetchall()
    groups = {}
    for row in incidents:
        key = (row[1], row[2], row[3])
        groups.setdefault(key, []).append(row[0])
    clusters = []
    for key, members in groups.items():
        if len(members) < 3:
            continue
        cid = uuid4()
        label = " / ".join(x or "unknown" for x in key)
        hypothesis = f"Recurring failure pattern around {label}"
        debt = failure_debt(1.0, min(1.0, len(members)/5), 0.5, 0.5)
        with connection() as conn:
            conn.execute("INSERT INTO recurrence_clusters(id,label,hypothesis,confidence) VALUES (%s,%s,%s,%s)", (cid,label,hypothesis,debt))
            for incident_id in members:
                conn.execute("INSERT INTO cluster_members(cluster_id,incident_id) VALUES (%s,%s) ON CONFLICT DO NOTHING", (cid,incident_id))
        clusters.append({"id":str(cid),"label":label,"members":len(members),"failure_debt":debt})
    return {"clusters":clusters}
