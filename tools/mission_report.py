from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = BASE_DIR / "reports"


def generate_report(state):

    mission = state["mission_data"]
    vision = state["vision_result"]
    risk = state["risk_result"]
    decision = state["final_decision"]
    safety = state["safety_result"]
    drone = state["drone_result"]

    timestamp = datetime.now()

    report = f"""
============================================================
AUTONOMOUS DRONE MISSION REPORT
============================================================

Timestamp:
{timestamp.strftime("%Y-%m-%d %H:%M:%S")}

-------------------- MISSION DATA --------------------------

Mission Request:
{state.get("question")}

Battery:
{mission.get("battery")}%

Wind Speed:
{mission.get("wind_speed")} km/h

GPS Available:
{mission.get("gps_status")}

-------------------- VISION ANALYSIS -----------------------

Inspection Type:
{vision.get("inspection_type")}

Anomaly Detected:
{vision.get("anomaly_detected")}

Anomaly Type:
{vision.get("anomaly_type")}

Confidence:
{vision.get("confidence", 0) * 100:.0f}%

Description:
{vision.get("description")}

-------------------- RISK ANALYSIS -------------------------

Risk Level:
{risk.get("risk_level")}

Detected Risks:
{risk.get("risks")}

Recommended Actions:
{risk.get("recommended_actions")}

-------------------- AI DECISION ----------------------------

Decision:
{decision.get("decision")}

Explanation:
{decision.get("explanation")}

RAG Evidence Sources:
{decision.get("evidence_count")}

-------------------- SAFETY GATE ---------------------------

Approved:
{safety.get("approved")}

Safety Action:
{safety.get("action")}

Safety Reason:
{safety.get("reason")}

-------------------- DRONE SIMULATOR -----------------------

Success:
{drone.get("success")}

Message:
{drone.get("message")}

============================================================
END OF MISSION REPORT
============================================================
"""

    # Create reports directory if it does not exist
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Create unique report filename
    filename = (
        f"mission_report_"
        f"{timestamp.strftime('%Y%m%d_%H%M%S')}.txt"
    )

    report_path = REPORT_DIR / filename

    # Save report
    with open(report_path, "w", encoding="utf-8") as file:
        file.write(report)

    print("\nMission report saved:")
    print(report_path)

    return report


if __name__ == "__main__":
    print("Mission report module loaded successfully.")