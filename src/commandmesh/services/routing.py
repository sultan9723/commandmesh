def choose_model(sensitivity: str) -> dict:
    sensitivity = sensitivity.lower()

    if sensitivity == "high":
        return {
            "selected_model": "private-llm",
            "reason": "High sensitivity request routed to private model"
        }

    if sensitivity == "medium":
        return {
            "selected_model": "gpt-4.1",
            "reason": "Medium sensitivity request routed to balanced model"
        }

    return {
        "selected_model": "gpt-4.1-mini",
        "reason": "Low sensitivity request routed to cost-efficient model"
    }