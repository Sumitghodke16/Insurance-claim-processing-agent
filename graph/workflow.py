from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from graph.state import ClaimState
from graph.routing import route_claim

from agents.document_agent import document_verification_agent
from agents.eligibility_agent import eligibility_check_agent
from agents.fraud_agent import fraud_detection_agent
from agents.summary_agent import claim_summary_agent
from agents.human_approval_agent import human_approval_agent


def approve_claim(state: ClaimState):
    """
    Final automatic approval node.
    """

    return {
        "decision": "APPROVED",
        "decision_reason": (
            "Claim passed document verification, "
            "eligibility checks, and fraud screening."
        ),
        "human_review_required": False,
    }


def reject_claim(state: ClaimState):
    """
    Final automatic rejection node.
    """

    reasons = []

    if not state.get("documents_valid", False):

        missing_documents = state.get(
            "missing_documents",
            []
        )

        if missing_documents:
            reasons.append(
                "Missing documents: "
                + ", ".join(missing_documents)
            )
        else:
            reasons.append(
                "Document verification failed."
            )

    if not state.get("policy_active", False):
        reasons.append(
            "Policy is inactive or not found."
        )

    if not state.get("claim_eligible", False):
        reasons.append(
            state.get(
                "eligibility_reason",
                "Claim is not eligible."
            )
        )

    return {
        "decision": "REJECTED",
        "decision_reason": " ".join(reasons),
        "human_review_required": False,
    }


def build_claim_workflow():

    workflow = StateGraph(ClaimState)

    # --------------------------------------------------
    # AGENT NODES
    # --------------------------------------------------

    workflow.add_node(
        "document_verification",
        document_verification_agent
    )

    workflow.add_node(
        "eligibility_check",
        eligibility_check_agent
    )

    workflow.add_node(
        "fraud_detection",
        fraud_detection_agent
    )

    workflow.add_node(
        "claim_summary",
        claim_summary_agent
    )

    # --------------------------------------------------
    # DECISION NODES
    # --------------------------------------------------

    workflow.add_node(
        "approve",
        approve_claim
    )

    workflow.add_node(
        "reject",
        reject_claim
    )

    workflow.add_node(
        "human_review",
        human_approval_agent
    )

    # --------------------------------------------------
    # START → PARALLEL AGENTS
    # --------------------------------------------------

    workflow.add_edge(
        START,
        "document_verification"
    )

    workflow.add_edge(
        START,
        "eligibility_check"
    )

    workflow.add_edge(
        START,
        "fraud_detection"
    )

    # --------------------------------------------------
    # PARALLEL AGENTS → SUMMARY
    # --------------------------------------------------

    workflow.add_edge(
        "document_verification",
        "claim_summary"
    )

    workflow.add_edge(
        "eligibility_check",
        "claim_summary"
    )

    workflow.add_edge(
        "fraud_detection",
        "claim_summary"
    )

    # --------------------------------------------------
    # SUMMARY → ROUTER
    # --------------------------------------------------

    workflow.add_conditional_edges(
        "claim_summary",
        route_claim,
        {
            "approve": "approve",
            "reject": "reject",
            "human_review": "human_review",
        }
    )

    # --------------------------------------------------
    # AUTOMATIC DECISION → END
    # --------------------------------------------------

    workflow.add_edge(
        "approve",
        END
    )

    workflow.add_edge(
        "reject",
        END
    )

    # --------------------------------------------------
    # HUMAN REVIEW → END
    # --------------------------------------------------

    workflow.add_edge(
        "human_review",
        END
    )

    # --------------------------------------------------
    # CHECKPOINTER
    # --------------------------------------------------

    checkpointer = MemorySaver()

    return workflow.compile(
        checkpointer=checkpointer
    )