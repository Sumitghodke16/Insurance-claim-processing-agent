from agents.document_agent import document_verification_agent


# Test Case 1
# Complete documents
valid_claim = {
    "claim_id": "CLM001",
    "claim_type": "vehicle_accident",
    "uploaded_documents": [
        "policy.pdf",
        "id_proof.pdf",

    ],
}


result = document_verification_agent(valid_claim)


print("\nDOCUMENT VERIFICATION TEST")
print("=" * 40)

print("Status:", result["document_result"]["status"])
print("Message:", result["document_result"]["message"])
print("Missing:", result["missing_documents"])
print("Workflow:", result["workflow_status"])