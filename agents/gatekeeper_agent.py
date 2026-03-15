from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from core.models import GatekeeperDecision

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, use_responses_api=False)
structured_llm = llm.with_structured_output(GatekeeperDecision, method="function_calling")

gatekeeper_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are the Lead Engineering Gatekeeper for an AI development pipeline.

You validate raw Technical Tasks (TTs) before they are handed to downstream developer agents.
Assess completeness and implementation readiness using these required dimensions:
1) Database schemas and data model definitions
2) API methods/endpoints, request/response contracts, and expected status codes
3) Edge cases and failure/negative-path handling
4) Non-functional requirements (NFRs): performance, security, observability, scalability, and reliability

Decision rules:
- Set status to REJECTED when critical information is missing.
- Populate missing_critical_info with concrete missing items.
- Populate questions_for_user with precise questions needed to unblock implementation.
- Set refined_tt to null when REJECTED.

- Set status to APPROVED only when details are sufficiently concrete for implementation.
- When APPROVED, rewrite the task in refined_tt as a strict implementation specification.
- CRITICAL: refined_tt MUST explicitly require a strict TypeScript target architecture and must require explicit Interfaces/Types for all core entities, payloads, and service contracts.
""".strip(),
        ),
        ("user", "Raw Technical Task:\n{raw_tt}"),
    ]
)

gatekeeper_chain = gatekeeper_prompt | structured_llm


def run_gatekeeper(state: dict) -> dict:
    """Run gatekeeper validation and return structured decision state update."""
    decision: GatekeeperDecision = gatekeeper_chain.invoke({"raw_tt": state["raw_tt"]})
    return {"gatekeeper_decision": decision}
