def safety_gate(decision, mission_data):
    """
    Final safety checkpoint before a drone action
    is executed.
    """

    print("\n" + "=" * 60)
    print("SAFETY GATE")
    print("=" * 60)

    battery = mission_data.get("battery", 100)

    # ------------------------------------------------
    # CRITICAL SAFETY OVERRIDE
    # ------------------------------------------------

    if battery < 10:

        print("\nCRITICAL BATTERY CONDITION")
        print("Automatic mission abort required.")

        return {
            "approved": True,
            "action": "ABORT_MISSION",
            "reason": "Battery below 10%"
        }

    # ------------------------------------------------
    # AUTOMATIC RETURN TO HOME
    # ------------------------------------------------

    if decision == "RETURN_TO_HOME":

        print("\nSafety rule triggered:")
        print("Battery below 20%.")

        return {
            "approved": True,
            "action": "RETURN_TO_HOME",
            "reason": "Battery safety threshold exceeded"
        }

    # ------------------------------------------------
    # HUMAN APPROVAL
    # ------------------------------------------------

    if decision == "HUMAN_REVIEW":

        print("\nHuman approval required.")

        approval = input(
            "\nApprove this action? (yes/no): "
        ).lower()

        if approval == "yes":

            return {
                "approved": True,
                "action": "APPROVED_BY_HUMAN",
                "reason": "Human approval received"
            }

        return {
            "approved": False,
            "action": "MISSION_BLOCKED",
            "reason": "Human approval denied"
        }

    # ------------------------------------------------
    # NORMAL MISSION
    # ------------------------------------------------

    if decision == "APPROVE":

        return {
            "approved": True,
            "action": "START_MISSION",
            "reason": "Safety checks passed"
        }

    # ------------------------------------------------
    # DEFAULT SAFE FALLBACK
    # ------------------------------------------------

    return {
        "approved": False,
        "action": "MISSION_BLOCKED",
        "reason": "Unknown or unsafe decision"
    }


# ====================================================
# TEST
# ====================================================

if __name__ == "__main__":

    mission = {
        "battery": 18,
        "wind_speed": 20,
        "gps_status": True
    }

    result = safety_gate(
        "RETURN_TO_HOME",
        mission
    )

    print("\n" + "=" * 60)
    print("SAFETY GATE RESULT")
    print("=" * 60)

    print(result)