"""
Integration tests for policy enforcement behavior.
"""

from fastapi.testclient import TestClient
import os

os.environ["MODEL_NAME"] = "test-model"

from app.main import app

client = TestClient(app)


def test_health_endpoint_returns_ok():
    """
    Verify the public health endpoint remains unchanged.
    """
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_secure_health_endpoint_returns_secure_ok():
    """
    Verify the protected health endpoint succeeds for an allowed action.
    """
    response = client.get("/secure-health")

    assert response.status_code == 200
    assert response.json() == {"status": "secure-ok"}


def test_secure_health_denied_returns_forbidden():
    """
    Verify the denial path returns a controlled 403 response.
    """
    response = client.get("/secure-health-denied")

    assert response.status_code == 403
    assert response.json() == {
        "detail": "Policy enforcement blocked the requested action.",
        "error": "Source 'external' is not permitted for this action.",
    }


def test_validate_agent_action_allows_read_status():
    """
    Verify a valid low-risk read action is approved.
    """
    response = client.post(
        "/agent/actions/validate",
        json={
            "action": "read_status",
            "resource": "service-health",
            "source": "agent",
            "parameters": {},
            "risk_level": "low",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": "approved",
        "action": "read_status",
        "resource": "service-health",
        "source": "agent",
    }


def test_validate_agent_action_denies_unapproved_deployment():
    """
    Verify a high-risk deployment is denied when approval is missing.
    """
    response = client.post(
        "/agent/actions/validate",
        json={
            "action": "deploy_model",
            "resource": "ml-service",
            "source": "agent",
            "parameters": {},
            "risk_level": "high",
        },
    )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "Policy enforcement blocked the requested action.",
        "error": "High-risk deployment requires explicit approval.",
    }


def test_validate_agent_action_allows_approved_deployment():
    """
    Verify a high-risk deployment is approved when explicit approval exists.
    """
    response = client.post(
        "/agent/actions/validate",
        json={
            "action": "deploy_model",
            "resource": "ml-service",
            "source": "agent",
            "parameters": {
                "approved": True,
            },
            "risk_level": "high",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": "approved",
        "action": "deploy_model",
        "resource": "ml-service",
        "source": "agent",
    }
