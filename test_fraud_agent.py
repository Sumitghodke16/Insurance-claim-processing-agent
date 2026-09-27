from agents.fraud_agent import fraud_detection_agent


def print_result(title, result):

    print("\n" + "=" * 55)
    print(title)
    print("=" * 55)

    print("Fraud Risk:", result["fraud_risk"])
    print(
        "Risk Score:",
        result["fraud_result"]["risk_score"]
    )

    print("Indicators:")

    for indicator in result["fraud_indicators"]:
        print(" -", indicator)

    print(
        "Workflow:",
        result["workflow_status"]
    )


# ============================================
# TEST 1 — NORMAL CLAIM
# ============================================

normal_claim = {

    "claim_amount": 45000,

    "documents_valid": True,

    "claim_eligible": True,

    "incident_description":
        "Vehicle was damaged in a road accident."
}

result = fraud_detection_agent(normal_claim)

print_result(
    "TEST 1 — NORMAL CLAIM",
    result
)


# ============================================
# TEST 2 — HIGH VALUE CLAIM
# ============================================

high_value_claim = {

    "claim_amount": 750000,

    "documents_valid": True,

    "claim_eligible": True,

    "incident_description":
        "Vehicle was damaged in a major accident."
}

result = fraud_detection_agent(high_value_claim)

print_result(
    "TEST 2 — HIGH VALUE CLAIM",
    result
)


# ============================================
# TEST 3 — MISSING DOCUMENTS
# ============================================

missing_documents_claim = {

    "claim_amount": 50000,

    "documents_valid": False,

    "claim_eligible": True,

    "incident_description":
        "Vehicle was damaged in a road accident."
}

result = fraud_detection_agent(
    missing_documents_claim
)

print_result(
    "TEST 3 — MISSING DOCUMENTS",
    result
)


# ============================================
# TEST 4 — SUSPICIOUS DESCRIPTION
# ============================================

suspicious_claim = {

    "claim_amount": 600000,

    "documents_valid": True,

    "claim_eligible": True,

    "incident_description":
        "The vehicle was intentionally damaged "
        "and the incident appears staged."
}

result = fraud_detection_agent(
    suspicious_claim
)

print_result(
    "TEST 4 — SUSPICIOUS CLAIM",
    result
)


# ============================================
# TEST 5 — MULTIPLE RISK FACTORS
# ============================================

very_high_risk_claim = {

    "claim_amount": 1500000,

    "documents_valid": False,

    "claim_eligible": False,

    "incident_description":
        "The incident appears fabricated and staged."
}

result = fraud_detection_agent(
    very_high_risk_claim
)

print_result(
    "TEST 5 — MULTIPLE RISK FACTORS",
    result
)