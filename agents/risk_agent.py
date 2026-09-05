def risk_agent(mission_data, vision_result=None):

    print("\n" + "=" * 60)
    print("RISK AGENT")
    print("=" * 60)

    battery = mission_data.get("battery", 100)
    wind_speed = mission_data.get("wind_speed", 0)
    gps_status = mission_data.get("gps_status", True)

    risks = []
    actions = []

    # ========================================================
    # BATTERY RISK
    # ========================================================

    if battery < 10:

        risks.append("CRITICAL: Battery below 10%")
        actions.append("ABORT_MISSION")

    elif battery < 20:

        risks.append("HIGH: Battery below 20%")
        actions.append("RETURN_TO_HOME")

    elif battery < 30:

        risks.append("MEDIUM: Battery below 30%")
        actions.append("MISSION_START_BLOCKED")

    # ========================================================
    # WIND RISK
    # ========================================================

    if wind_speed > 30:

        risks.append(
            f"HIGH: Wind speed is {wind_speed} km/h"
        )

        actions.append("PAUSE_OR_RETURN")

    # ========================================================
    # GPS RISK
    # ========================================================

    if not gps_status:

        risks.append("HIGH: GPS unavailable")
        actions.append("PAUSE_OR_RETURN")

    # ========================================================
    # VISION / VLM RISK
    # ========================================================

    if vision_result:

        anomaly = vision_result.get(
            "anomaly_detected",
            False
        )

        confidence = vision_result.get(
            "confidence",
            0
        )

        anomaly_type = vision_result.get(
            "anomaly_type",
            "unknown"
        )

        if anomaly:

            if confidence >= 0.80:

                risks.append(
                    f"HIGH: Vision detected {anomaly_type} "
                    f"with high confidence"
                )

                actions.append(
                    "SECONDARY_INSPECTION"
                )

            elif confidence >= 0.70:

                risks.append(
                    f"MEDIUM: Vision detected {anomaly_type} "
                    f"with moderate confidence"
                )

                actions.append(
                    "HUMAN_REVIEW"
                )

            else:

                risks.append(
                    f"MEDIUM: Possible {anomaly_type} "
                    f"with low confidence"
                )

                actions.append(
                    "HUMAN_REVIEW"
                )

    # ========================================================
    # OVERALL RISK LEVEL
    # ========================================================

    if any(
        "CRITICAL" in risk
        for risk in risks
    ):

        risk_level = "CRITICAL"

    elif any(
        "HIGH" in risk
        for risk in risks
    ):

        risk_level = "HIGH"

    elif any(
        "MEDIUM" in risk
        for risk in risks
    ):

        risk_level = "MEDIUM"

    else:

        risk_level = "LOW"

    # ========================================================
    # RESULT
    # ========================================================

    result = {
        "risk_level": risk_level,
        "risks": risks,
        "recommended_actions": actions
    }

    # ========================================================
    # DISPLAY
    # ========================================================

    print(f"\nBattery: {battery}%")
    print(f"Wind Speed: {wind_speed} km/h")
    print(f"GPS Status: {gps_status}")

    if vision_result:

        print(
            f"Vision Anomaly: "
            f"{vision_result.get('anomaly_detected')}"
        )

        print(
            f"Vision Type: "
            f"{vision_result.get('anomaly_type')}"
        )

        print(
            f"Vision Confidence: "
            f"{vision_result.get('confidence', 0) * 100:.0f}%"
        )

    print(f"\nRisk Level: {risk_level}")

    if risks:

        print("\nDetected Risks:")

        for risk in risks:
            print(f"- {risk}")

    if actions:

        print("\nRecommended Actions:")

        for action in actions:
            print(f"- {action}")

    return result


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    mission = {
        "battery": 80,
        "wind_speed": 15,
        "gps_status": True
    }

    vision = {
        "anomaly_detected": True,
        "anomaly_type": "thermal_anomaly",
        "confidence": 0.86
    }

    result = risk_agent(
        mission,
        vision
    )

    print("\n" + "=" * 60)
    print("RISK RESULT")
    print("=" * 60)

    print(result)