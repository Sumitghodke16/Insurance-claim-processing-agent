from typing import Dict, Any, List


# Required documents for an insurance claim
REQUIRED_DOCUMENTS = {
    "vehicle_accident": [
        "policy.pdf",
        "id_proof.pdf",
        "fir.pdf",
        "repair_estimate.pdf",
    ],
    "health": [
        "policy.pdf",
        "id_proof.pdf",
        "medical_bill.pdf",
        "medical_report.pdf",
    ],
    "property": [
        "policy.pdf",
        "id_proof.pdf",
        "damage_report.pdf",
        "repair_estimate.pdf",
    ],
}


def normalize_filename(filename: str) -> str:
    """
    Convert a filename into a standard format.

    Example:
        'Policy.PDF' -> 'policy.pdf'
    """
    return filename.strip().lower()


def document_verification_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Verify whether all required documents are available.

    Reads:
        claim_type
        uploaded_documents

    Returns:
        document_result
        documents_valid
        missing_documents
        workflow_status
    """

    claim_type = state.get("claim_type", "").strip().lower()

    uploaded_documents: List[str] = [
        normalize_filename(doc)
        for doc in state.get("uploaded_documents", [])
    ]

    # Get required documents for this claim type
    required_documents = REQUIRED_DOCUMENTS.get(
        claim_type,
        REQUIRED_DOCUMENTS["vehicle_accident"]
    )

    # Find missing documents
    missing_documents = [
        document
        for document in required_documents
        if document not in uploaded_documents
    ]

    documents_valid = len(missing_documents) == 0

    if documents_valid:
        status = "PASS"
        message = "All required documents are available."
    else:
        status = "FAIL"
        message = "One or more required documents are missing."

    result = {
        "status": status,
        "message": message,
        "required_documents": required_documents,
        "uploaded_documents": uploaded_documents,
        "missing_documents": missing_documents,
    }

    return {
        "document_result": result,
        "documents_valid": documents_valid,
        "missing_documents": missing_documents,
        
    }