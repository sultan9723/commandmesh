from src.commandmesh.models.route import RouteRequest, SensitivityLevel
from src.commandmesh.services.policy import evaluate_policy
from src.commandmesh.services.routing import process_route_request


def test_high_sensitivity_blocked_for_developer():
    request = RouteRequest(
        prompt="Summarize this patient record",
        sensitivity=SensitivityLevel.high,
        user_role="developer"
    )

    result = evaluate_policy(request)

    assert result["allowed"] is False
    assert result["status"] == "blocked"


def test_high_sensitivity_allowed_for_security():
    request = RouteRequest(
        prompt="Review this security incident",
        sensitivity=SensitivityLevel.high,
        user_role="security"
    )

    result = evaluate_policy(request)

    assert result["allowed"] is True
    assert result["status"] == "approved"


def test_route_request_returns_blocked_response():
    request = RouteRequest(
        prompt="Access sensitive internal medical data",
        sensitivity=SensitivityLevel.high,
        user_role="developer"
    )

    result = process_route_request(request)

    assert result["allowed"] is False
    assert result["status"] == "blocked"
    assert result["selected_model"] is None