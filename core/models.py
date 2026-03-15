from pydantic import BaseModel, Field
from typing import List, Optional

class GatekeeperDecision(BaseModel):
    """The strict JSON structure the Gatekeeper MUST output."""
    
    status: str = Field(
        description="Must be exactly 'APPROVED' or 'REJECTED'"
    )
    missing_critical_info: List[str] = Field(
        description="List of missing technical details, like DB schema or APIs. Leave empty if APPROVED.",
        default=[]
    )
    questions_for_user: List[str] = Field(
        description="Questions to ask the user to fix the TT. Leave empty if APPROVED.",
        default=[]
    )
    refined_tt: Optional[str] = Field(
        description="If APPROVED, the perfectly rewritten technical prompt for the dev agents. Null if REJECTED.",
        default=None
    )