import streamlit as st
from langgraph.types import Command

from graph.workflow import build_claim_workflow


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Insurance Claim Processing Agent",
    page_icon="🛡️",
    layout="wide",
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "workflow_app" not in st.session_state:
    st.session_state.workflow_app = build_claim_workflow()

if "claim_result" not in st.session_state:
    st.session_state.claim_result = None

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

if "waiting_for_human" not in st.session_state:
    st.session_state.waiting_for_human = False

if "review_data" not in st.session_state:
    st.session_state.review_data = None


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🛡️ Insurance Claim Processing Agent")

st.markdown(
    """
    **AI-powered insurance claim workflow using LangGraph + Gemini**

    The system performs document verification, policy eligibility
    checks, fraud detection, claim summarization, conditional
    routing, and human-in-the-loop review.
    """
)

st.divider()


# --------------------------------------------------
# CLAIM INPUT
# --------------------------------------------------

st.header("📋 Claim Information")

col1, col2 = st.columns(2)

with col1:

    claim_id = st.text_input(
        "Claim ID",
        value="CLM001"
    )

    policy_id = st.text_input(
        "Policy ID",
        value="POL001"
    )

    customer_name = st.text_input(
        "Customer Name",
        value="Rahul Sharma"
    )

    claim_type = st.selectbox(
        "Claim Type",
        [
            "vehicle_accident",
            "health",
            "property",
        ]
    )


with col2:

    claim_amount = st.number_input(
        "Claim Amount (₹)",
        min_value=0.0,
        value=45000.0,
        step=5000.0,
    )

    incident_description = st.text_area(
        "Incident Description",
        value=(
            "The insured vehicle was involved in a road accident "
            "and sustained front-end damage."
        ),
        height=150,
    )


# --------------------------------------------------
# DOCUMENT UPLOAD
# --------------------------------------------------

st.header("📄 Claim Documents")

uploaded_files = st.file_uploader(
    "Upload claim documents",
    type=["pdf"],
    accept_multiple_files=True,
)

if uploaded_files:

    st.write("Uploaded documents:")

    for file in uploaded_files:
        st.write(f"📄 {file.name}")

else:

    st.info(
        "Upload the required PDF documents before processing "
        "the claim."
    )


# --------------------------------------------------
# PROCESS CLAIM
# --------------------------------------------------

st.divider()

process_claim = st.button(
    "🚀 Process Claim",
    type="primary",
    use_container_width=True,
)


if process_claim:

    if not claim_id.strip():
        st.error("Please enter a Claim ID.")

    elif not policy_id.strip():
        st.error("Please enter a Policy ID.")

    elif not customer_name.strip():
        st.error("Please enter the customer name.")

    elif not incident_description.strip():
        st.error("Please enter an incident description.")

    else:

        # --------------------------------------------------
        # DOCUMENT FILENAMES
        # --------------------------------------------------

        uploaded_documents = [
            file.name
            for file in uploaded_files
        ] if uploaded_files else []


        # --------------------------------------------------
        # INITIAL STATE
        # --------------------------------------------------

        initial_state = {

            "claim_id": claim_id.strip(),

            "policy_id": policy_id.strip(),

            "customer_name": customer_name.strip(),

            "claim_type": claim_type,

            "claim_amount": float(claim_amount),

            "incident_description": (
                incident_description.strip()
            ),

            "uploaded_documents": uploaded_documents,

            "workflow_status": "INITIALIZED",
        }


        # --------------------------------------------------
        # THREAD ID
        # --------------------------------------------------

        thread_id = f"claim-{claim_id.strip()}"

        st.session_state.thread_id = thread_id


        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }


        # --------------------------------------------------
        # RUN WORKFLOW
        # --------------------------------------------------

        with st.spinner(
            "Processing insurance claim..."
        ):

            try:

                result = (
                    st.session_state.workflow_app.invoke(
                        initial_state,
                        config=config,
                    )
                )


                # --------------------------------------------------
                # HUMAN REVIEW INTERRUPT
                # --------------------------------------------------

                if "__interrupt__" in result:

                    interrupt_data = (
                        result["__interrupt__"][0].value
                    )

                    st.session_state.review_data = (
                        interrupt_data
                    )

                    st.session_state.waiting_for_human = True

                    st.session_state.claim_result = result

                else:

                    st.session_state.claim_result = result

                    st.session_state.waiting_for_human = False

                    st.session_state.review_data = None


            except Exception as e:

                st.error(
                    f"Workflow error: {e}"
                )


# --------------------------------------------------
# HUMAN REVIEW
# --------------------------------------------------

if st.session_state.waiting_for_human:

    review_data = st.session_state.review_data

    st.divider()

    st.warning(
        "⚠️ Human Review Required"
    )

    st.subheader(
        "Fraud Risk Assessment"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Claim ID",
            review_data.get(
                "claim_id",
                "N/A"
            )
        )

    with col2:

        st.metric(
            "Fraud Risk",
            review_data.get(
                "fraud_risk",
                "UNKNOWN"
            )
        )


    st.write(
        f"**Claim Amount:** "
        f"₹{review_data.get('claim_amount', 0):,.2f}"
    )


    st.write("**Fraud Indicators:**")

    for indicator in review_data.get(
        "fraud_indicators",
        []
    ):

        st.write(
            f"• {indicator}"
        )


    st.info(
        review_data.get(
            "message",
            "Human approval is required."
        )
    )


    st.subheader(
        "Human Decision"
    )

    col1, col2 = st.columns(2)


    with col1:

        approve_button = st.button(
            "✅ Approve Claim",
            use_container_width=True,
        )


    with col2:

        reject_button = st.button(
            "❌ Reject Claim",
            use_container_width=True,
        )


    if approve_button or reject_button:

        human_decision = (
            "APPROVE"
            if approve_button
            else "REJECT"
        )


        config = {
            "configurable": {
                "thread_id": (
                    st.session_state.thread_id
                )
            }
        }


        with st.spinner(
            "Applying human decision..."
        ):

            try:

                final_result = (
                    st.session_state.workflow_app.invoke(
                        Command(
                            resume=human_decision
                        ),
                        config=config,
                    )
                )


                st.session_state.claim_result = (
                    final_result
                )

                st.session_state.waiting_for_human = (
                    False
                )

                st.session_state.review_data = None

                st.rerun()


            except Exception as e:

                st.error(
                    f"Unable to resume workflow: {e}"
                )


# --------------------------------------------------
# DISPLAY FINAL RESULT
# --------------------------------------------------

result = st.session_state.claim_result


if result and not st.session_state.waiting_for_human:

    st.divider()

    st.header("📊 Claim Assessment")

    # --------------------------------------------------
    # STATUS METRICS
    # --------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        documents_valid = result.get(
            "documents_valid",
            False
        )

        st.metric(
            "Documents",
            "PASS"
            if documents_valid
            else "FAIL"
        )


    with col2:

        eligible = result.get(
            "claim_eligible",
            False
        )

        st.metric(
            "Eligibility",
            "PASS"
            if eligible
            else "FAIL"
        )


    with col3:

        st.metric(
            "Fraud Risk",
            result.get(
                "fraud_risk",
                "UNKNOWN"
            )
        )


    with col4:

        decision = result.get(
            "decision",
            "UNKNOWN"
        )

        st.metric(
            "Decision",
            decision
        )


    # --------------------------------------------------
    # DECISION
    # --------------------------------------------------

    decision = result.get(
        "decision",
        "UNKNOWN"
    )


    if decision == "APPROVED":

        st.success(
            "✅ Claim Approved"
        )

    elif decision == "REJECTED":

        st.error(
            "❌ Claim Rejected"
        )

    elif decision == "HUMAN_REVIEW":

        st.warning(
            "⚠️ Human Review Required"
        )


    # --------------------------------------------------
    # DECISION REASON
    # --------------------------------------------------

    st.subheader(
        "Decision Reason"
    )

    st.write(
        result.get(
            "decision_reason",
            "No decision reason available."
        )
    )


    # --------------------------------------------------
    # DOCUMENT RESULTS
    # --------------------------------------------------

    with st.expander(
        "📄 Document Verification"
    ):

        st.write(
            "**Status:**",
            "PASS"
            if result.get(
                "documents_valid",
                False
            )
            else "FAIL"
        )

        missing_documents = result.get(
            "missing_documents",
            []
        )

        if missing_documents:

            st.write(
                "**Missing Documents:**"
            )

            for document in missing_documents:

                st.write(
                    f"• {document}"
                )

        else:

            st.write(
                "All required documents are available."
            )


    # --------------------------------------------------
    # ELIGIBILITY RESULTS
    # --------------------------------------------------

    with st.expander(
        "📋 Policy Eligibility"
    ):

        st.write(
            "**Policy Active:**",
            result.get(
                "policy_active",
                False
            )
        )

        st.write(
            "**Claim Eligible:**",
            result.get(
                "claim_eligible",
                False
            )
        )

        st.write(
            "**Reason:**",
            result.get(
                "eligibility_reason",
                "N/A"
            )
        )


    # --------------------------------------------------
    # FRAUD RESULTS
    # --------------------------------------------------

    with st.expander(
        "🔍 Fraud Assessment"
    ):

        fraud_result = result.get(
            "fraud_result",
            {}
        )

        st.write(
            "**Risk Level:**",
            result.get(
                "fraud_risk",
                "UNKNOWN"
            )
        )

        st.write(
            "**Risk Score:**",
            fraud_result.get(
                "risk_score",
                0
            )
        )

        st.write(
            "**Indicators:**"
        )

        for indicator in result.get(
            "fraud_indicators",
            []
        ):

            st.write(
                f"• {indicator}"
            )


    # --------------------------------------------------
    # AI SUMMARY
    # --------------------------------------------------

    with st.expander(
        "🤖 AI Claim Summary",
        expanded=True,
    ):

        st.markdown(
            result.get(
                "claim_summary",
                "No summary available."
            )
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Insurance Claim Processing Agent • "
    "LangGraph + Gemini + Streamlit"
)