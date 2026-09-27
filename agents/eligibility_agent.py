import json
from pathlib import Path
from typing import Dict, Any


# Get project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Path to policies.json
POLICIES_FILE = PROJECT_ROOT / "data" / "policies.json"


def load_policies():
    """
    Load all insurance policies from policies.json.
    """
    with open(POLICIES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def find_policy(policy_id: str):
    """
    Find a policy using the policy ID.
    """
    policies = load_policies()

    for policy in policies:
        if policy["policy_id"].lower() == policy_id.lower():
            return policy

    return None


def eligibility_check_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check whether an insurance claim is eligible.

    Checks:
    1. Policy exists
    2. Policy is active
    3. Claim type is covered
    4. Claim amount is within policy limit
    """

    policy_id = state.get("policy_id", "")
    claim_type = state.get("claim_type", "").strip().lower()
    claim_amount = float(state.get("claim_amount", 0))

    # Find policy
    policy = find_policy(policy_id)

    # --------------------------------------------------
    # CHECK 1: POLICY EXISTS
    # --------------------------------------------------
    if policy is None:

        return {
            "policy_result": {
                "status": "FAIL",
                "reason": "Policy not found.",
                "policy_id": policy_id,
            },

            "policy_active": False,

            "claim_eligible": False,

            "eligibility_reason": "Policy does not exist.",
        }

    # --------------------------------------------------
    # CHECK 2: POLICY IS ACTIVE
    # --------------------------------------------------
    if policy["status"].lower() != "active":

        return {
            "policy_result": {
                "status": "FAIL",
                "reason": "Policy is expired or inactive.",
                "policy_id": policy_id,
                "policy_status": policy["status"],
            },

            "policy_active": False,

            "claim_eligible": False,

            "eligibility_reason": (
                "Policy is expired or inactive."
            ),
        }

    # --------------------------------------------------
    # CHECK 3: CLAIM TYPE IS COVERED
    # --------------------------------------------------
    if claim_type not in policy["coverage"]:

        return {
            "policy_result": {
                "status": "FAIL",
                "reason": "Claim type is not covered by the policy.",
                "policy_id": policy_id,
                "coverage": policy["coverage"],
            },

            "policy_active": True,

            "claim_eligible": False,

            "eligibility_reason": (
                "Claim type is not covered by the policy."
            ),
        }

    # --------------------------------------------------
    # CHECK 4: CLAIM AMOUNT WITHIN POLICY LIMIT
    # --------------------------------------------------
    maximum_claim = float(
        policy["maximum_claim_amount"]
    )

    if claim_amount > maximum_claim:

        return {
            "policy_result": {
                "status": "FAIL",
                "reason": "Claim amount exceeds policy limit.",
                "policy_id": policy_id,
                "maximum_claim_amount": maximum_claim,
                "requested_amount": claim_amount,
            },

            "policy_active": True,

            "claim_eligible": False,

            "eligibility_reason": (
                f"Claim amount ₹{claim_amount:,.2f} exceeds "
                f"policy limit ₹{maximum_claim:,.2f}."
            ),
        }

    # --------------------------------------------------
    # ALL CHECKS PASSED
    # --------------------------------------------------
    return {
        "policy_result": {
            "status": "PASS",
            "reason": "Policy is active and claim is covered.",
            "policy_id": policy_id,
            "policy_status": policy["status"],
            "coverage": policy["coverage"],
            "maximum_claim_amount": maximum_claim,
            "requested_amount": claim_amount,
        },

        "policy_active": True,

        "claim_eligible": True,

        "eligibility_reason": (
            "Claim is eligible under the policy."
        ),
    }