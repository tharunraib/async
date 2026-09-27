from app.schemas import PolicyDecision

def decide(action: str, trusted: bool = False) -> PolicyDecision:
    if not trusted:
        return PolicyDecision(allowed=False, reason="Action requires explicit policy approval")
    return PolicyDecision(allowed=True, reason=f"Policy permits action: {action}")
