from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class GatekeeperDecision(BaseModel):
    """Structured decision emitted by the Gatekeeper agent."""

    status: Literal["APPROVED", "REJECTED"] = Field(
        description="Must be exactly 'APPROVED' or 'REJECTED'."
    )
    missing_critical_info: List[str] = Field(
        default_factory=list,
        description="Missing technical details that block implementation.",
    )
    questions_for_user: List[str] = Field(
        default_factory=list,
        description="Clarifying questions for the user.",
    )
    refined_tt: Optional[str] = Field(
        default=None,
        description="Rewritten strict TypeScript technical task when approved.",
    )
