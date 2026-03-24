from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.security.exceptions import PolicyViolationError
from app.security.models import ActionRequest, AgentActionInput
from app.security.policy_engine import (
    PolicyEngine,
    allow_agent_read_status,
    gate_high_risk_deployment,
)

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(name)s:%(message)s",
)

# Load and validate configuration at startup.
# Invalid configuration should stop the service before the API begins serving traffic.
settings = get_settings()

app = FastAPI(
    title="Secure ML Deployment Pipeline",
    description="Minimal FastAPI service for secure ML deployment demonstration.",
    version="0.1.0",
)

# Central policy engine used to enforce protected actions.
policy_engine = PolicyEngine()

# Baseline rule:
# allow the read_status action only from approved sources.
policy_engine.register_policy("read_status", allow_agent_read_status)

# High-risk rule:
# deployment-style actions require explicit approval.
policy_engine.register_policy("deploy_model", gate_high_risk_deployment)


@app.get("/health")
def health_check() -> dict[str, str]:
    """
    Health endpoint used for local validation, container smoke tests,
    and deployment checks.
    """
    return {"status": "ok"}


@app.exception_handler(PolicyViolationError)
def handle_policy_violation(
    request: Request, exception: PolicyViolationError
) -> JSONResponse:
    """
    Return a controlled HTTP response when policy enforcement blocks an action.

    This prevents raw internal exceptions from leaking through the API surface
    while keeping denial behavior explicit and machine-readable.
    """

    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "detail": "Policy enforcement blocked the requested action.",
            "error": str(exception),
        },
    )


@app.get("/secure-health")
def secure_health_check() -> dict[str, str]:
    """
    Protected health endpoint.

    This route demonstrates how agent-triggered or protected actions
    are evaluated by the policy layer before a response is returned.
    """

    request = ActionRequest(
        action="read_status",
        resource="service-health",
        source="agent",
        parameters={},
        risk_level="low",
    )

    policy_engine.enforce(request)

    return {"status": "secure-ok"}


@app.get("/secure-health-denied")
def secure_health_denied() -> dict[str, str]:
    """
    Negative-path validation endpoint.

    This route intentionally submits a disallowed source so the policy
    violation handler can be tested through a real API request.
    """

    request = ActionRequest(
        action="read_status",
        resource="service-health",
        source="external",
        parameters={},
        risk_level="low",
    )

    policy_engine.enforce(request)

    return {"status": "should-not-return"}


@app.post("/agent/actions/validate")
def validate_agent_action(payload: AgentActionInput) -> dict[str, str]:
    """
    Validate and enforce an externally supplied agent action.

    This route creates a clean boundary between untrusted API input and the
    trusted internal ActionRequest model used by the policy layer.
    """

    # Convert validated external input into the internal enforcement model.
    request = ActionRequest(
        action=payload.action,
        resource=payload.resource,
        source=payload.source,
        parameters=payload.parameters,
        risk_level=payload.risk_level,
    )

    # Enforce registered policy rules before approval is returned.
    policy_engine.enforce(request)

    return {
        "status": "approved",
        "action": request.action,
        "resource": request.resource,
        "source": request.source,
    }
