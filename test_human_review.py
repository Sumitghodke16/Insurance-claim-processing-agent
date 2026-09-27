from graph.workflow import build_claim_workflow


initial_state = {
    "claim_id": "CLM003",
    "policy_id": "POL001",
    "customer_name": "Rahul Sharma",
    "claim_type": "vehicle_accident",

    # Multiple fraud indicators
    "claim_amount": 500000,

    "incident_description": (
        "The vehicle was intentionally damaged and the incident "
        "appears to be staged and fabricated."
    ),

    "uploaded_documents": [
        "policy.pdf",
        "id_proof.pdf",
        "fir.pdf",
        "repair_estimate.pdf",
    ],

    "workflow_status": "INITIALIZED",
}


print("\nHUMAN REVIEW WORKFLOW TEST")
print("=" * 70)


app = build_claim_workflow()

final_state = app.invoke(initial_state)


print("\nClaim ID:")
print(final_state.get("claim_id"))

print("\nDocuments Valid:")
print(final_state.get("documents_valid"))

print("\nClaim Eligible:")
print(final_state.get("claim_eligible"))

print("\nFraud Risk:")
print(final_state.get("fraud_risk"))

print("\nFraud Score:")
print(final_state.get("fraud_result", {}).get("risk_score"))

print("\nFraud Indicators:")

for indicator in final_state.get("fraud_indicators", []):
    print("-", indicator)


print("\nDecision:")
print(final_state.get("decision"))

print("\nDecision Reason:")
print(final_state.get("decision_reason"))

print("\nHuman Review Required:")
print(final_state.get("human_review_required", False))


print("\n" + "=" * 70)
print("WORKFLOW COMPLETED")
print("=" * 70)