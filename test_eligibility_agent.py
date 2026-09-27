from agents.eligibility_agent import eligibility_check_agent


def print_result(title, result):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)

    print("Policy Active:", result["policy_active"])
    print("Claim Eligible:", result["claim_eligible"])
    print("Reason:", result["eligibility_reason"])
    print("Status:", result["policy_result"]["status"])


# ============================================
# TEST 1 — VALID ACTIVE POLICY
# ============================================

valid_claim = {
    "policy_id": "POL001",
    "claim_type": "vehicle_accident",
    "claim_amount": 45000
}

result = eligibility_check_agent(valid_claim)

print_result(
    "TEST 1 — VALID ACTIVE POLICY",
    result
)


# ============================================
# TEST 2 — EXPIRED POLICY
# ============================================

expired_claim = {
    "policy_id": "POL002",
    "claim_type": "vehicle_accident",
    "claim_amount": 45000
}

result = eligibility_check_agent(expired_claim)

print_result(
    "TEST 2 — EXPIRED POLICY",
    result
)


# ============================================
# TEST 3 — CLAIM ABOVE POLICY LIMIT
# ============================================

high_value_claim = {
    "policy_id": "POL004",
    "claim_type": "vehicle_accident",
    "claim_amount": 150000
}

result = eligibility_check_agent(high_value_claim)

print_result(
    "TEST 3 — CLAIM ABOVE POLICY LIMIT",
    result
)


# ============================================
# TEST 4 — WRONG COVERAGE
# ============================================

wrong_coverage_claim = {
    "policy_id": "POL001",
    "claim_type": "hospitalization",
    "claim_amount": 50000
}

result = eligibility_check_agent(wrong_coverage_claim)

print_result(
    "TEST 4 — WRONG COVERAGE",
    result
)


# ============================================
# TEST 5 — POLICY NOT FOUND
# ============================================

unknown_policy_claim = {
    "policy_id": "POL999",
    "claim_type": "vehicle_accident",
    "claim_amount": 50000
}

result = eligibility_check_agent(unknown_policy_claim)

print_result(
    "TEST 5 — POLICY NOT FOUND",
    result
)