def decision_agent(rag_evidence, risk_result, mission_data):
    """
    Decision Agent:
    Combines retrieved knowledge and safety analysis
    to produce the final mission decision.
    """

    print("\n" + "=" * 60)
    print("DECISION AGENT")
    print("=" * 60)

    battery = mission_data.get("battery", 100)

    risk_level = risk_result.get(
        "risk_level",
        "UNKNOWN"
    )

    risks = risk_result.get(
        "risks",
        []
    )

    recommended_actions = risk_result.get(
        "recommended_actions",
        []
    )

    # ------------------------------------------------
    # SAFETY-FIRST DECISION LOGIC
    # ------------------------------------------------

    if battery < 10:

        decision = "ABORT_MISSION"
        explanation = (
            "Battery is below 10%. "
            "Mission must be aborted and emergency "
            "landing performed when safe."
        )

    elif "RETURN_TO_HOME" in recommended_actions:

        decision = "RETURN_TO_HOME"
        explanation = (
            "Battery is below 20%. "
            "Drone must immediately initiate RTH."
        )

    elif "MISSION_START_BLOCKED" in recommended_actions:

        decision = "MISSION_START_BLOCKED"
        explanation = (
            "Battery is below the minimum required "
            "level to start a new mission."
        )

    elif risk_level == "HIGH":

        decision = "HUMAN_REVIEW"
        explanation = (
            "High-risk condition detected. "
            "Human approval is required."
        )

    elif risk_level == "MEDIUM":

        decision = "HUMAN_REVIEW"
        explanation = (
            "Medium-risk condition detected. "
            "Human review is recommended."
        )

    else:

        decision = "APPROVE"
        explanation = (
            "No critical safety risks were detected."
        )

    # ------------------------------------------------
    # BUILD FINAL RESULT
    # ------------------------------------------------

    result = {
        "decision": decision,
        "risk_level": risk_level,
        "explanation": explanation,
        "risks": risks,
        "recommended_actions": recommended_actions,
        "evidence_count": len(rag_evidence)
    }

    # ------------------------------------------------
    # DISPLAY RESULT
    # ------------------------------------------------

    print(f"\nRisk Level: {risk_level}")

    print(f"\nFinal Decision: {decision}")

    print(f"\nExplanation:")
    print(explanation)

    if risks:

        print("\nRisks:")

        for risk in risks:
            print(f"- {risk}")

    print(
        f"\nRAG Evidence Used: "
        f"{len(rag_evidence)} sources"
    )

    return result


# ====================================================
# TEST
# ====================================================

if __name__ == "__main__":

    sample_evidence = [
        {
            "source": "drone_safety_policy.txt",
            "content": (
                "Battery below 20% requires "
                "Return-to-Home."
            )
        }
    ]

    sample_risk = {
        "risk_level": "HIGH",
        "risks": [
            "HIGH: Battery below 20%"
        ],
        "recommended_actions": [
            "RETURN_TO_HOME"
        ]
    }

    sample_mission = {
        "battery": 18,
        "wind_speed": 20,
        "gps_status": True
    }

    result = decision_agent(
        sample_evidence,
        sample_risk,
        sample_mission
    )

    print("\n" + "=" * 60)
    print("FINAL DECISION RESULT")
    print("=" * 60)

    print(result)