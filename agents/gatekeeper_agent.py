import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from core.models import GatekeeperDecision

# Load your API keys from the .env file
load_dotenv()

# 1. Initialize the LLM (Using OpenAI's fast and cheap model for the Gatekeeper)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 2. Force the LLM to reply using our strict JSON structure
structured_llm = llm.with_structured_output(GatekeeperDecision)

# 3. The System Prompt (Notice how we strictly enforce TypeScript here)
gatekeeper_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are the Lead Engineering Gatekeeper. Your job is to intercept raw Technical Tasks (TTs) 
    and rewrite them into highly technical, hallucination-free prompts for junior AI developer agents.
    
    CRITICAL RULE: The target tech stack for the generated code is strictly TYPESCRIPT.
    
    Analyze the user's TT against these criteria:
    1. Are Data Schemas defined? (e.g., TypeScript Interfaces, Prisma schemas, DTO's, or TypeORM entities)
    2. Are API methods, endpoints, and HTTP status codes defined?
    3. Are negative paths and edge cases handled?
    
    If the TT is missing critical details, set status to 'REJECTED' and ask the user questions.
    If the TT is acceptable, set status to 'APPROVED' and rewrite the requirement in 'refined_tt'.
    
    When writing the 'refined_tt', you must specify that the output should be in strict TypeScript, 
    including exact Interfaces/Types for the data models.
    """),
    ("user", "Here is the raw Technical Task from the analyst: {raw_tt}")
])

# 4. Create the Chain (Prompt -> LLM)
gatekeeper_chain = gatekeeper_prompt | structured_llm

# 5. The actual function our LangGraph router will call
def run_gatekeeper(state: dict):
    """Takes the current state, runs the Gatekeeper, and updates the decision."""
    
    print("--- 🛡️ GATEKEEPER ANALYZING TASK ---")
    raw_tt = state["raw_tt"]
    
    # Run the LLM chain
    decision: GatekeeperDecision = gatekeeper_chain.invoke({"raw_tt": raw_tt})
    
    # Return the updated state
    return {"gatekeeper_decision": decision}