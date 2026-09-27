from langgraph.types import Command

from graph.workflow import build_claim_workflow


initial_state = {
    "claim_id": "CLM003",
    "policy_id": "POL001",
    "customer_name": "Rahul Sharma",
    "claim_type": "vehicle_accident",

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


print("\nHUMAN-IN-THE-LOOP TEST")
print("=" * 70)


app = build_claim_workflow()


# Unique ID for this workflow execution.
config = {
    "configurable": {
        "thread_id": "claim-CLM003"
    }
}


# --------------------------------------------------
# FIRST RUN
# --------------------------------------------------

result = app.invoke(
    initial_state,
    config=config
)


print("\nWorkflow paused for human review.")


# --------------------------------------------------
# CHECK INTERRUPT
# --------------------------------------------------

if "__interrupt__" in result:

    interrupt_data = result["__interrupt__"][0].value

    print("\nHUMAN REVIEW REQUEST")
    print("-" * 70)

    print("Claim ID:")
    print(interrupt_data["claim_id"])

    print("\nClaim Amount:")
    print(
        f"₹{interrupt_data['claim_amount']:,.2f}"
    )

    print("\nFraud Risk:")
    print(interrupt_data["fraud_risk"])

    print("\nFraud Indicators:")

    for indicator in interrupt_data["fraud_indicators"]:
        print("-", indicator)

    print("\nMessage:")
    print(interrupt_data["message"])

    print("-" * 70)

    human_decision = input(
        "\nEnter human decision (APPROVE/REJECT): "
    ).strip().upper()


    # --------------------------------------------------
    # RESUME WORKFLOW
    # --------------------------------------------------

    result = app.invoke(
        Command(
            resume=human_decision
        ),
        config=config
    )


# --------------------------------------------------
# FINAL RESULT
# --------------------------------------------------

print("\nFINAL WORKFLOW RESULT")
print("=" * 70)

print("Decision:")
print(result.get("decision"))

print("\nHuman Review Required:")
print(
    result.get(
        "human_review_required",
        False
    )
)

print("\nHuman Approval:")
print(
    result.get(
        "human_approval"
    )
)

print("\nDecision Reason:")
print(
    result.get(
        "decision_reason"
    )
)

print("=" * 70)