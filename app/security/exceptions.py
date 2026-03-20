"""
Custom exceptions used by the security policy layer.
"""


class PolicyViolationError(Exception):
    """
    Raised when a requested action violates an enforced security policy.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
