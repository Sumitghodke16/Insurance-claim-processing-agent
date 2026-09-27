from typing import TypedDict, List, Dict, Any, Optional


class ClaimState(TypedDict, total=False):

    # =========================
    # CLAIM INFORMATION
    # =========================

    claim_id: str
    policy_id: str
    customer_name: str
    claim_type: str
    claim_amount: float
    incident_description: str

    # =========================
    # DOCUMENT INFORMATION
    # =========================

    uploaded_documents: List[str]

    document_result: Dict[str, Any]
    documents_valid: bool
    missing_documents: List[str]

    # =========================
    # ELIGIBILITY INFORMATION
    # =========================

    policy_result: Dict[str, Any]
    policy_active: bool
    claim_eligible: bool
    eligibility_reason: str

    # =========================
    # FRAUD INFORMATION
    # =========================

    fraud_result: Dict[str, Any]
    fraud_risk: str
    fraud_indicators: List[str]

    # =========================
    # SUMMARY
    # =========================

    claim_summary: str

    # =========================
    # FINAL DECISION
    # =========================

    decision: str
    decision_reason: str

    # =========================
    # HUMAN APPROVAL
    # =========================

    human_review_required: bool
    human_approval: Optional[str]

    # =========================
    # WORKFLOW STATUS
    # =========================

    workflow_status: str