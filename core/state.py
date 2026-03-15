import operator
from typing import Annotated, TypedDict

from core.models import GatekeeperDecision


class AgentState(TypedDict):
    """Shared graph state passed between nodes."""

    raw_tt: str
    gatekeeper_decision: GatekeeperDecision
    messages: Annotated[list, operator.add]
