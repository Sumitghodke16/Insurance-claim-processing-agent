from typing import Dict, Any

from langgraph.types import interrupt


def human_approval_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Pause the LangGraph workflow and request a human decision.

    The workflow resumes when a human provides:
        APPROVE
    or
        REJECT
    """

    fraud_risk = state.get("fraud_risk", "UNKNOWN")
    fraud_indicators = state.get("fraud_indicators", [])
    claim_id = state.get("claim_id", "UNKNOWN")
    claim_amount = state.get("claim_amount", 0)

    review_request = {
        "claim_id": claim_id,
        "claim_amount": claim_amount,
        "fraud_risk": fraud_risk,
        "fraud_indicators": fraud_indicators,
        "message": (
            "Human approval is required because the claim "
            "has HIGH fraud risk."
        ),
    }

    # Pause the workflow.
    human_decision = interrupt(review_request)

    # Normalize the human response.
    if isinstance(human_decision, str):
        decision = human_decision.strip().upper()
    elif isinstance(human_decision, dict):
        decision = str(
            human_decision.get("decision", "")
        ).strip().upper()
    else:
        decision = ""

    # Validate decision.
    if decision not in {"APPROVE", "REJECT"}:
        raise ValueError(
            "Invalid human decision. "
            "Expected APPROVE or REJECT."
        )

    if decision == "APPROVE":
        return {
            "decision": "APPROVED",
            "human_review_required": True,
            "human_approval": "APPROVED",
            "decision_reason": (
                "Claim was manually approved after human review."
            ),
        }

    return {
        "decision": "REJECTED",
        "human_review_required": True,
        "human_approval": "REJECTED",
        "decision_reason": (
            "Claim was manually rejected after human review."
        ),
    }