import hashlib, json
from app.db import connection

def append_event(event_type: str, payload: dict):
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    with connection() as conn:
        row = conn.execute("SELECT event_hash FROM audit_events ORDER BY id DESC LIMIT 1").fetchone()
        previous = row[0] if row else "GENESIS"
        event_hash = hashlib.sha256((previous + canonical).encode()).hexdigest()
        conn.execute(
            "INSERT INTO audit_events(event_type,payload,previous_hash,event_hash) VALUES (%s,%s,%s,%s)",
            (event_type, payload, previous, event_hash),
        )
    return {"event_hash": event_hash, "previous_hash": previous}
