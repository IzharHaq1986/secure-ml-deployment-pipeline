"""
Pydantic models used by the policy enforcement layer.
"""

from typing import Any, Dict, Literal

from pydantic import BaseModel, ConfigDict, Field


class ActionRequest(BaseModel):
    """
    Internal trusted model used by the policy enforcement layer.

    This model represents an action after external input has already been
    validated and transformed into an internal enforcement object.
    """

    action: str = Field(
        ...,
        description="Logical action being requested, such as read_status.",
    )
    resource: str = Field(
        ...,
        description="Target resource associated with the requested action.",
    )
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Optional action parameters supplied with the request.",
    )
    source: str = Field(
        ...,
        description="Origin of the request, such as agent, user, or system.",
    )
    risk_level: str = Field(
        default="low",
        description="Declared risk level for the requested action.",
    )


class AgentActionInput(BaseModel):
    """
    External input model for agent-submitted actions.

    This model represents untrusted request data received through the API.
    Validation is intentionally strict so only known-safe fields and values
    can enter the policy enforcement path.
    """

    model_config = ConfigDict(extra="forbid")

    action: Literal["read_status", "deploy_model"] = Field(
        ...,
        description="Allowed external action name.",
    )
    resource: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Target resource associated with the requested action.",
    )
    source: Literal["agent", "system", "external"] = Field(
        ...,
        description="Declared origin of the request.",
    )
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Optional request parameters.",
    )
    risk_level: Literal["low", "medium", "high"] = Field(
        default="low",
        description="Declared risk level for the request.",
    )
