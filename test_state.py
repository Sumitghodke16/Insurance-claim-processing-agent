from graph.state import ClaimState


test_claim: ClaimState = {
    "claim_id": "CLM001",
    "policy_id": "POL001",
    "customer_name": "Rahul Sharma",
    "claim_type": "Vehicle Accident",
    "claim_amount": 45000,
    "incident_description": "Vehicle damaged in a road accident.",
    "uploaded_documents": [
        "policy.pdf",
        "id_proof.pdf",
        "fir.pdf",
        "repair_estimate.pdf"
    ],
    "workflow_status": "INITIALIZED"
}


print("Claim State Created Successfully!")
print("--------------------------------")
print("Claim ID:", test_claim["claim_id"])
print("Policy ID:", test_claim["policy_id"])
print("Customer:", test_claim["customer_name"])
print("Amount:", test_claim["claim_amount"])
print("Status:", test_claim["workflow_status"])