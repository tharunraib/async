import re

COMPONENT_RE = re.compile(r"(?:component|service|module)[:= ]+([\\w.-]+)", re.I)
DEPENDENCY_RE = re.compile(r"(?:dependency|depends on|upstream)[:= ]+([\\w.-]+)", re.I)
OWNER_RE = re.compile(r"(?:owner|team)[:= ]+([\\w.-]+)", re.I)


def fingerprint(body: str, component=None, symptom=None, dependency=None, owner=None):
    def pick(value, pattern):
        if value:
            return value.strip()
        match = pattern.search(body)
        return match.group(1).strip() if match else None

    return {
        "component": pick(component, COMPONENT_RE),
        "symptom": symptom or _symptom(body),
        "dependency": pick(dependency, DEPENDENCY_RE),
        "owner": pick(owner, OWNER_RE),
    }


def _symptom(body: str):
    lowered = body.lower()
    known = ["timeout", "connection pool", "5xx", "latency", "oom", "deadlock", "authentication", "rate limit", "queue backlog"]
    for item in known:
        if item in lowered:
            return item
    return "unknown"
