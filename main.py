from typing import TypedDict

from langgraph.graph import StateGraph, END

from agents.rag_agent import rag_agent
from agents.vision_agent import vision_agent
from agents.risk_agent import risk_agent
from agents.decision_agent import decision_agent

from safety.safety_gate import safety_gate

from tools.drone_simulator import DroneSimulator
from tools.mission_memory import save_mission
from tools.mission_report import generate_report


# ============================================================
# DRONE STATE
# ============================================================

class DroneState(TypedDict):
    question: str
    mission_data: dict
    rag_evidence: list
    vision_result: dict
    risk_result: dict
    final_decision: dict
    safety_result: dict
    drone_result: dict


# ============================================================
# RAG NODE
# ============================================================

def rag_node(state):

    print("\n" + "=" * 60)
    print("LANGGRAPH → RAG NODE")
    print("=" * 60)

    evidence = rag_agent(
        state["question"]
    )

    return {
        "rag_evidence": evidence
    }


# ============================================================
# VISION NODE
# ============================================================

def vision_node(state):

    print("\n" + "=" * 60)
    print("LANGGRAPH → VISION NODE")
    print("=" * 60)

    image_path = (
        "data/images/sample_drone_image.png"
    )

    result = vision_agent(
        image_path
    )

    return {
        "vision_result": result
    }


# ============================================================
# RISK NODE
# ============================================================

def risk_node(state):

    print("\n" + "=" * 60)
    print("LANGGRAPH → RISK NODE")
    print("=" * 60)

    risk = risk_agent(
        state["mission_data"],
        state["vision_result"]
    )

    return {
        "risk_result": risk
    }


# ============================================================
# DECISION NODE
# ============================================================

def decision_node(state):

    print("\n" + "=" * 60)
    print("LANGGRAPH → DECISION NODE")
    print("=" * 60)

    decision = decision_agent(
        state["rag_evidence"],
        state["risk_result"],
        state["mission_data"]
    )

    return {
        "final_decision": decision
    }


# ============================================================
# SAFETY NODE
# ============================================================

def safety_node(state):

    print("\n" + "=" * 60)
    print("LANGGRAPH → SAFETY GATE")
    print("=" * 60)

    decision = state["final_decision"]["decision"]

    result = safety_gate(
        decision,
        state["mission_data"]
    )

    return {
        "safety_result": result
    }


# ============================================================
# DRONE NODE
# ============================================================

def drone_node(state):

    print("\n" + "=" * 60)
    print("LANGGRAPH → DRONE SIMULATOR")
    print("=" * 60)

    mission_data = state["mission_data"]

    drone = DroneSimulator(
        battery=mission_data["battery"],
        wind_speed=mission_data["wind_speed"],
        gps_status=mission_data["gps_status"]
    )

    action = state["safety_result"]["action"]

    print(f"\nExecuting action: {action}")

    if action == "START_MISSION":

        result = drone.start_mission()

    elif action == "RETURN_TO_HOME":

        result = drone.return_to_home()

    elif action == "ABORT_MISSION":

        result = drone.abort_mission()

    elif action == "PAUSE_MISSION":

        result = drone.pause_mission()

    elif action == "APPROVED_BY_HUMAN":

        result = drone.start_mission()

    elif action == "MISSION_BLOCKED":

        result = {
            "success": False,
            "message": "Mission blocked by safety gate."
        }

    else:

        result = {
            "success": False,
            "message": "Unknown safety action."
        }

    return {
        "drone_result": result
    }


# ============================================================
# BUILD LANGGRAPH
# ============================================================

def build_graph():

    workflow = StateGraph(
        DroneState
    )

    workflow.add_node(
        "rag",
        rag_node
    )

    workflow.add_node(
        "vision",
        vision_node
    )

    workflow.add_node(
        "risk",
        risk_node
    )

    workflow.add_node(
        "decision",
        decision_node
    )

    workflow.add_node(
        "safety",
        safety_node
    )

    workflow.add_node(
        "drone",
        drone_node
    )

    workflow.set_entry_point(
        "rag"
    )

    workflow.add_edge(
        "rag",
        "vision"
    )

    workflow.add_edge(
        "vision",
        "risk"
    )

    workflow.add_edge(
        "risk",
        "decision"
    )

    workflow.add_edge(
        "decision",
        "safety"
    )

    workflow.add_edge(
        "safety",
        "drone"
    )

    workflow.add_edge(
        "drone",
        END
    )

    return workflow.compile()


# ============================================================
# RUN MISSION
# ============================================================

def run_mission():

    print("\n")
    print("=" * 70)
    print(" AUTONOMOUS DRONE MISSION INTELLIGENCE SYSTEM")
    print("=" * 70)

    print("\nEnter mission details.")

    # --------------------------------------------------------
    # Mission question
    # --------------------------------------------------------

    question = input(
        "\nWhat should the drone system check? "
    )

    # --------------------------------------------------------
    # Battery
    # --------------------------------------------------------

    battery = int(
        input(
            "Enter battery percentage: "
        )
    )

    # --------------------------------------------------------
    # Wind
    # --------------------------------------------------------

    wind_speed = float(
        input(
            "Enter wind speed (km/h): "
        )
    )

    # --------------------------------------------------------
    # GPS
    # --------------------------------------------------------

    gps_input = input(
        "Is GPS available? (yes/no): "
    ).lower()

    gps_status = (
        gps_input == "yes"
    )

    # --------------------------------------------------------
    # Mission data
    # --------------------------------------------------------

    mission_data = {
        "battery": battery,
        "wind_speed": wind_speed,
        "gps_status": gps_status
    }

    # --------------------------------------------------------
    # Initial state
    # --------------------------------------------------------

    initial_state = {

        "question": question,

        "mission_data": mission_data,

        "rag_evidence": [],

        "vision_result": {},

        "risk_result": {},

        "final_decision": {},

        "safety_result": {},

        "drone_result": {}
    }

    # --------------------------------------------------------
    # Build graph
    # --------------------------------------------------------

    graph = build_graph()

    print("\n")
    print("=" * 70)
    print("STARTING AGENTIC WORKFLOW")
    print("=" * 70)

    # --------------------------------------------------------
    # Execute graph
    # --------------------------------------------------------

    final_state = graph.invoke(
        initial_state
    )

    # ========================================================
    # FINAL REPORT
    # ========================================================

    print("\n")
    print("=" * 70)
    print("FINAL MISSION REPORT")
    print("=" * 70)

    # --------------------------------------------------------
    # Mission
    # --------------------------------------------------------

    print("\nMISSION DATA")
    print("-" * 40)

    print(
        f"Mission Request: "
        f"{final_state['question']}"
    )

    print(
        f"Battery: "
        f"{final_state['mission_data']['battery']}%"
    )

    print(
        f"Wind Speed: "
        f"{final_state['mission_data']['wind_speed']} km/h"
    )

    print(
        f"GPS Available: "
        f"{final_state['mission_data']['gps_status']}"
    )

    # --------------------------------------------------------
    # Vision
    # --------------------------------------------------------

    print("\nVISION ANALYSIS")
    print("-" * 40)

    vision = final_state[
        "vision_result"
    ]

    print(
        f"Anomaly Detected: "
        f"{vision.get('anomaly_detected')}"
    )

    print(
        f"Anomaly Type: "
        f"{vision.get('anomaly_type')}"
    )

    print(
        f"Confidence: "
        f"{vision.get('confidence', 0) * 100:.0f}%"
    )

    print(
        f"Description: "
        f"{vision.get('description')}"
    )

    # --------------------------------------------------------
    # Risk
    # --------------------------------------------------------

    print("\nRISK ANALYSIS")
    print("-" * 40)

    risk = final_state[
        "risk_result"
    ]

    print(
        f"Risk Level: "
        f"{risk.get('risk_level')}"
    )

    print(
        f"Detected Risks: "
        f"{risk.get('risks')}"
    )

    print(
        f"Recommended Actions: "
        f"{risk.get('recommended_actions')}"
    )

    # --------------------------------------------------------
    # Decision
    # --------------------------------------------------------

    print("\nAI DECISION")
    print("-" * 40)

    decision = final_state[
        "final_decision"
    ]

    print(
        f"Decision: "
        f"{decision.get('decision')}"
    )

    print(
        f"Explanation: "
        f"{decision.get('explanation')}"
    )

    print(
        f"RAG Evidence Used: "
        f"{decision.get('evidence_count')}"
    )

    # --------------------------------------------------------
    # Safety
    # --------------------------------------------------------

    print("\nSAFETY GATE")
    print("-" * 40)

    safety = final_state[
        "safety_result"
    ]

    print(
        f"Approved: "
        f"{safety.get('approved')}"
    )

    print(
        f"Safety Action: "
        f"{safety.get('action')}"
    )

    print(
        f"Reason: "
        f"{safety.get('reason')}"
    )

    # --------------------------------------------------------
    # Drone
    # --------------------------------------------------------

    print("\nDRONE SIMULATOR")
    print("-" * 40)

    drone_result = final_state[
        "drone_result"
    ]

    print(
        f"Success: "
        f"{drone_result.get('success')}"
    )

    print(
        f"Message: "
        f"{drone_result.get('message')}"
    )

    # ========================================================
    # SAVE MISSION
    # ========================================================

    save_mission(
        mission_data,
        decision.get("decision"),
        risk.get("risk_level"),
        drone_result
    )

    # ========================================================
    # GENERATE REPORT
    # ========================================================

    report = generate_report(
        final_state
    )

    print("\n")
    print("=" * 70)
    print("GENERATED MISSION REPORT")
    print("=" * 70)

    print(report)

    # ========================================================
    # COMPLETE
    # ========================================================

    print("\n")
    print("=" * 70)
    print("MISSION COMPLETED SUCCESSFULLY")
    print("=" * 70)


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    run_mission()