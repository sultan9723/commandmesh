from src.commandmesh.models.route import RouteRequest


ALLOWED_HIGH_SENSITIVITY_ROLES = {"security", "admin", "compliance"}


def evaluate_policy(request: RouteRequest) -> dict:
    role = request.user_role.strip().lower()
    sensitivity = request.sensitivity.value

    if sensitivity == "high" and role not in ALLOWED_HIGH_SENSITIVITY_ROLES:
        return {
            "allowed": False,
            "status": "pending",
            "reason": f"Role '{role}' is not permitted to submit high-sensitivity requests. Sent for approval."
        }

    return {
        "allowed": True,
        "status": "approved",
        "reason": "Request passed policy checks"
    }