"""
Central policy enforcement logic for agent-triggered actions.
"""

import logging
from collections.abc import Callable
from typing import Dict

from app.security.exceptions import PolicyViolationError
from app.security.models import ActionRequest

logger = logging.getLogger(__name__)

PolicyValidator = Callable[[ActionRequest], None]


class PolicyEngine:
    """
    Centralized policy engine.

    Every protected action should pass through this layer before execution.
    Unknown actions are denied by default.
    """

    def __init__(self) -> None:
        self._policies: Dict[str, PolicyValidator] = {}

    def register_policy(self, action: str, validator: PolicyValidator) -> None:
        """
        Register a validator function for a named action.
        """
        self._policies[action] = validator

    def enforce(self, request: ActionRequest) -> None:
        """
        Evaluate a request against the registered policy for its action.

        Raises:
            PolicyViolationError:
                If the action is not registered or fails validation.
        """
        validator = self._policies.get(request.action)

        if validator is None:
            logger.warning(
                "policy_decision=denied action=%s resource=%s source=%s "
                "risk_level=%s reason=%s",
                request.action,
                request.resource,
                request.source,
                request.risk_level,
                "unregistered_action",
            )
            raise PolicyViolationError(
                f"Action '{request.action}' is not allowed."
            )

        try:
            validator(request)
        except PolicyViolationError as exception:
            logger.warning(
                "policy_decision=denied action=%s resource=%s source=%s "
                "risk_level=%s reason=%s",
                request.action,
                request.resource,
                request.source,
                request.risk_level,
                str(exception),
            )
            raise

        logger.info(
            "policy_decision=approved action=%s resource=%s source=%s "
            "risk_level=%s",
            request.action,
            request.resource,
            request.source,
            request.risk_level,
        )


def allow_agent_read_status(request: ActionRequest) -> None:
    """
    Baseline read-only policy.

    This policy allows only the read_status action from approved sources.
    """
    allowed_sources = {"agent", "system"}

    if request.action != "read_status":
        raise PolicyViolationError(
            "Only the 'read_status' action is permitted by this policy."
        )

    if request.source not in allowed_sources:
        raise PolicyViolationError(
            f"Source '{request.source}' is not permitted for this action."
        )


def gate_high_risk_deployment(request: ActionRequest) -> None:
    """
    High-risk deployment policy.

    This policy blocks deployment-style actions unless the request:
    - uses the deploy_model action
    - originates from the agent source
    - explicitly declares high risk
    - includes an explicit approval flag
    """

    if request.action != "deploy_model":
        raise PolicyViolationError(
            "This policy only handles the 'deploy_model' action."
        )

    if request.source != "agent":
        raise PolicyViolationError(
            "Only the 'agent' source is permitted for deployment requests."
        )

    if request.risk_level != "high":
        raise PolicyViolationError(
            "Deployment requests must declare a 'high' risk level."
        )

    approved = request.parameters.get("approved", False)

    if approved is not True:
        raise PolicyViolationError(
            "High-risk deployment requires explicit approval."
        )
