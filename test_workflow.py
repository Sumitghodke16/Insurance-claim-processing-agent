from graph.workflow import build_claim_workflow


initial_state = {
    "claim_id": "CLM002",
    "policy_id": "POL002",
    "customer_name": "Amit Patil",
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

    "workflow_status": "INITIALIZED",
}


print("\nStarting Insurance Claim Workflow...")
print("=" * 70)


app = build_claim_workflow()

final_state = app.invoke(initial_state)


print("\nINSURANCE CLAIM WORKFLOW TEST")
print("=" * 70)

print("\nClaim ID:")
print(final_state.get("claim_id"))

print("\nDocuments Valid:")
print(final_state.get("documents_valid"))

print("\nClaim Eligible:")
print(final_state.get("claim_eligible"))

print("\nFraud Risk:")
print(final_state.get("fraud_risk"))

print("\nMissing Documents:")
print(final_state.get("missing_documents", []))

print("\nEligibility Reason:")
print(final_state.get("eligibility_reason"))

print("\nFraud Indicators:")

for indicator in final_state.get("fraud_indicators", []):
    print("-", indicator)


print("\nClaim Summary:")
print(final_state.get("claim_summary"))


print("\nWorkflow Status:")
print(final_state.get("workflow_status"))


print("\nDecision:")
print(final_state.get("decision"))


print("\nDecision Reason:")
print(final_state.get("decision_reason"))


print("\nHuman Review Required:")
print(final_state.get("human_review_required", False))


print("\n" + "=" * 70)
print("WORKFLOW COMPLETED")
print("=" * 70)