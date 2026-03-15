from src.commandmesh.models.route import RouteRequest
from src.commandmesh.services.audit import record_audit_event
from src.commandmesh.services.policy import evaluate_policy


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


def process_route_request(request: RouteRequest) -> dict:
    policy_result = evaluate_policy(request)

    if not policy_result["allowed"]:
        result = {
            "prompt": request.prompt,
            "user_role": request.user_role,
            "sensitivity": request.sensitivity.value,
            "selected_model": None,
            "reason": policy_result["reason"],
            "status": "blocked",
            "allowed": False
        }

        record_audit_event(result)
        return result

    routing_result = choose_model(request.sensitivity.value)

    result = {
        "prompt": request.prompt,
        "user_role": request.user_role,
        "sensitivity": request.sensitivity.value,
        "selected_model": routing_result["selected_model"],
        "reason": routing_result["reason"],
        "status": "routed",
        "allowed": True
    }

    record_audit_event(result)
    return result