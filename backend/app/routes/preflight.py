from fastapi import APIRouter
from app.db import connection
from app.schemas import PreflightRequest
from app.services.audit import append_event

router = APIRouter(tags=["preflight"])

@router.post("/preflight")
def preflight(req: PreflightRequest):
    with connection() as conn:
        rows = conn.execute(
            """SELECT rc.id,rc.label,rc.hypothesis,rc.confidence
               FROM recurrence_clusters rc
               WHERE EXISTS (
                 SELECT 1 FROM cluster_members cm JOIN incidents i ON i.id=cm.incident_id
                 WHERE cm.cluster_id=rc.id AND i.component = ANY(%s)
               )""", (req.components,)
        ).fetchall()
    warning = len(rows) > 0
    result = {"warning": warning, "matches":[{"cluster_id":str(r[0]),"label":r[1],"hypothesis":r[2],"confidence":r[3]} for r in rows], "change":req.change_title}
    append_event("preflight.checked", result)
    return result
