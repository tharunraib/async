from fastapi import APIRouter
from app.db import connection
from app.schemas import SearchRequest

router = APIRouter(tags=["retrieval"])

@router.post("/retrieval/search")
def search(req: SearchRequest):
    terms = req.query.strip().split()
    tsquery = " & ".join(t for t in terms if t)
    with connection() as conn:
        rows = conn.execute(
            """SELECT i.id,i.external_id,i.title,c.content,ts_rank(c.search_vector, plainto_tsquery('english', %s)) AS score
               FROM chunks c JOIN incidents i ON i.id=c.incident_id
               WHERE c.search_vector @@ plainto_tsquery('english', %s)
               ORDER BY score DESC LIMIT %s""",
            (req.query, req.query, req.limit),
        ).fetchall()
    return [{"incident_id":str(r[0]),"external_id":r[1],"title":r[2],"evidence":r[3],"score":float(r[4])} for r in rows]
