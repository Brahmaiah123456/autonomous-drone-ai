from agents.risk_agent import risk_agent
from agents.decision_agent import decision_agent
from safety.safety_gate import safety_gate


def run_test(name, mission):

    print("\n" + "=" * 70)
    print(f"TEST: {name}")
    print("=" * 70)

    print("\nMission:")
    print(mission)

    # Risk Agent
    risk = risk_agent(mission)

    # Simulated RAG evidence
    evidence = [
        {
            "source": "drone_safety_policy.txt",
            "content": "Safety policy used for testing."
        }
    ]

    # Decision Agent
    decision = decision_agent(
        evidence,
        risk,
        mission
    )

    # Safety Gate
    #
    # For HUMAN_REVIEW we automatically approve in this
    # automated test so the test does not stop for input.
    if decision["decision"] == "HUMAN_REVIEW":

        print("\nAutomated test:")
        print("Human review required → simulated approval.")

        safety = {
            "approved": True,
            "action": "APPROVED_BY_HUMAN",
            "reason": "Simulated human approval for automated testing."
        }

    else:

        safety = safety_gate(
            decision["decision"],
            mission
        )

    print("\nFINAL RESULT")
    print("-" * 50)

    print(
        "Risk:",
        risk["risk_level"]
    )

    print(
        "Decision:",
        decision["decision"]
    )

    print(
        "Safety Action:",
        safety["action"]
    )

    return {
        "risk": risk,
        "decision": decision,
        "safety": safety
    }


# ============================================================
# TEST 1 — NORMAL MISSION
# ============================================================

run_test(
    "Normal Mission",
    {
        "battery": 80,
        "wind_speed": 15,
        "gps_status": True
    }
)


# ============================================================
# TEST 2 — LOW BATTERY
# ============================================================

run_test(
    "Low Battery",
    {
        "battery": 18,
        "wind_speed": 20,
        "gps_status": True
    }
)


# ============================================================
# TEST 3 — CRITICAL BATTERY
# ============================================================

run_test(
    "Critical Battery",
    {
        "battery": 8,
        "wind_speed": 20,
        "gps_status": True
    }
)


# ============================================================
# TEST 4 — UNSAFE WIND
# ============================================================

run_test(
    "Unsafe Wind",
    {
        "battery": 80,
        "wind_speed": 40,
        "gps_status": True
    }
)


# ============================================================
# TEST 5 — GPS FAILURE
# ============================================================

run_test(
    "GPS Failure",
    {
        "battery": 80,
        "wind_speed": 15,
        "gps_status": False
    }
)


print("\n")
print("=" * 70)
print("ALL MISSION TESTS COMPLETED")
print("=" * 70)