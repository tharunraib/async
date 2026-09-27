def failure_debt(recurrence: float, persistence: float, impact: float, spread: float) -> float:
    values = [max(0.0, min(1.0, x)) for x in (recurrence, persistence, impact, spread)]
    return round(sum(values) / 4.0, 4)
