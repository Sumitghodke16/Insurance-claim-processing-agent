from typing import Dict, Any


def route_claim(state: Dict[str, Any]) -> str:
    """
    Determine the next workflow route based on deterministic
    insurance claim business rules.
    """

    documents_valid = state.get("documents_valid", False)
    policy_active = state.get("policy_active", False)
    claim_eligible = state.get("claim_eligible", False)
    fraud_risk = state.get("fraud_risk", "HIGH").upper()

    # --------------------------------------------------
    # REJECT CONDITIONS
    # --------------------------------------------------

    if not documents_valid:
        return "reject"

    if not policy_active:
        return "reject"

    if not claim_eligible:
        return "reject"

    # --------------------------------------------------
    # HUMAN REVIEW CONDITION
    # --------------------------------------------------

    if fraud_risk == "HIGH":
        return "human_review"

    # --------------------------------------------------
    # APPROVE
    # --------------------------------------------------

    return "approve"