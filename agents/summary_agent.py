from typing import Dict, Any

from utils.llm import get_llm


def claim_summary_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    llm = get_llm()

    claim_id = state.get("claim_id", "N/A")
    customer_name = state.get("customer_name", "N/A")
    claim_type = state.get("claim_type", "N/A")
    claim_amount = state.get("claim_amount", 0)
    incident_description = state.get("incident_description", "")

    documents_valid = state.get("documents_valid", False)
    missing_documents = state.get("missing_documents", [])

    claim_eligible = state.get("claim_eligible", False)
    eligibility_reason = state.get(
        "eligibility_reason",
        "No eligibility reason available."
    )

    fraud_risk = state.get("fraud_risk", "UNKNOWN")
    fraud_indicators = state.get("fraud_indicators", [])

    prompt = f"""
You are an insurance claim processing assistant.

Create a concise professional claim assessment summary.

Claim Information:
- Claim ID: {claim_id}
- Customer: {customer_name}
- Claim Type: {claim_type}
- Claim Amount: ₹{claim_amount:,.2f}
- Incident Description: {incident_description}

Document Verification:
- Documents Valid: {documents_valid}
- Missing Documents: {missing_documents}

Eligibility:
- Claim Eligible: {claim_eligible}
- Eligibility Reason: {eligibility_reason}

Fraud Assessment:
- Fraud Risk: {fraud_risk}
- Fraud Indicators: {fraud_indicators}

Write the summary using these sections:

1. Claim Overview
2. Document Verification
3. Eligibility Assessment
4. Fraud Assessment
5. Overall Assessment

Do not invent information that is not provided.
Keep the summary factual and concise.
"""
    response = llm.invoke(prompt)

    if isinstance(response.content, str):
        summary = response.content

    elif isinstance(response.content, list):
        text_parts = []

        for block in response.content:
            if isinstance(block, dict) and block.get("type") == "text":
                text_parts.append(block.get("text", ""))

        summary = "\n".join(text_parts).strip()

    else:
        summary = str(response.content)

    return {
        "claim_summary": summary,
        "workflow_status": "CLAIM_SUMMARY_COMPLETED",
    }