from agents.summary_agent import claim_summary_agent


test_state = {
    "claim_id": "CLM001",
    "policy_id": "POL001",
    "customer_name": "Rahul Sharma",
    "claim_type": "vehicle_accident",
    "claim_amount": 45000,
    "incident_description": (
        "The insured vehicle was involved in a road accident "
        "and sustained front-end damage."
    ),

    "uploaded_documents": [
        "policy.pdf",
        "id_proof.pdf",
        "fir.pdf",
        "repair_estimate.pdf",
    ],

    "documents_valid": True,
    "missing_documents": [],

    "policy_active": True,
    "claim_eligible": True,
    "eligibility_reason": "Claim is eligible under the policy.",

    "fraud_risk": "LOW",
    "fraud_indicators": [
        "No significant fraud indicators detected."
    ],
}


result = claim_summary_agent(test_state)


print("\nCLAIM SUMMARY AGENT TEST")
print("=" * 60)

print(result["claim_summary"])

print("=" * 60)
print("Workflow:", result["workflow_status"])