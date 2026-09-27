from typing import Dict, Any, List


def fraud_detection_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze a claim for potential fraud indicators.

    The agent uses transparent business rules rather than
    a trained machine-learning model.

    Checks:
    1. Claim amount
    2. Missing documents
    3. Eligibility result
    4. Suspicious claim amount
    5. Inconsistencies in claim information
    """

    claim_amount = float(state.get("claim_amount", 0))

    documents_valid = state.get("documents_valid", True)

    claim_eligible = state.get("claim_eligible", True)

    incident_description = (
        state.get("incident_description", "")
        .strip()
        .lower()
    )

    fraud_indicators: List[str] = []

    risk_score = 0

    # ==========================================
    # RULE 1 — VERY HIGH CLAIM AMOUNT
    # ==========================================

    if claim_amount >= 1000000:

        fraud_indicators.append(
            "Claim amount is extremely high."
        )

        risk_score += 3

    elif claim_amount >= 500000:

        fraud_indicators.append(
            "Claim amount is unusually high."
        )

        risk_score += 2

    elif claim_amount >= 250000:

        fraud_indicators.append(
            "Claim amount is relatively high."
        )

        risk_score += 1

    # ==========================================
    # RULE 2 — MISSING DOCUMENTS
    # ==========================================

    if not documents_valid:

        fraud_indicators.append(
            "Required claim documents are missing."
        )

        risk_score += 2

    # ==========================================
    # RULE 3 — CLAIM NOT ELIGIBLE
    # ==========================================

    if not claim_eligible:

        fraud_indicators.append(
            "Claim failed the policy eligibility check."
        )

        risk_score += 2

    # ==========================================
    # RULE 4 — SUSPICIOUS WORDS IN DESCRIPTION
    # ==========================================

    suspicious_terms = [
        "fake",
        "duplicate",
        "staged",
        "fraud",
        "false",
        "fabricated",
        "intentionally damaged",
    ]

    found_terms = [
        term
        for term in suspicious_terms
        if term in incident_description
    ]

    if found_terms:

        fraud_indicators.append(
            "Incident description contains potentially "
            "suspicious terms: "
            + ", ".join(found_terms)
        )

        risk_score += 3

    # ==========================================
    # DETERMINE FINAL RISK
    # ==========================================

    if risk_score >= 5:

        fraud_risk = "HIGH"

    elif risk_score >= 2:

        fraud_risk = "MEDIUM"

    else:

        fraud_risk = "LOW"

    # ==========================================
    # NO INDICATORS
    # ==========================================

    if not fraud_indicators:

        fraud_indicators.append(
            "No significant fraud indicators detected."
        )

    # ==========================================
    # RESULT
    # ==========================================

    result = {
        "risk_level": fraud_risk,
        "risk_score": risk_score,
        "fraud_indicators": fraud_indicators,
    }

    return {
        "fraud_result": result,
        "fraud_risk": fraud_risk,
        "fraud_indicators": fraud_indicators,
        "workflow_status": "FRAUD_DETECTION_COMPLETED",
    }