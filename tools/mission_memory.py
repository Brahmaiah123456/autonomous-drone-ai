import json
from pathlib import Path
from datetime import datetime


MEMORY_FILE = Path(__file__).resolve().parent.parent / "data" / "mission_memory.json"


def save_mission(mission_data, decision, risk_level, drone_result):
    """Save a completed mission for future reference."""

    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            missions = json.load(file)
    else:
        missions = []

    mission_record = {
        "timestamp": datetime.now().isoformat(),
        "mission": mission_data,
        "risk_level": risk_level,
        "decision": decision,
        "drone_result": drone_result
    }

    missions.append(mission_record)

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(
            missions,
            file,
            indent=4
        )

    print("\nMission saved to memory.")


def get_mission_history():
    """Return previously saved missions."""

    if not MEMORY_FILE.exists():
        return []

    with open(MEMORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


if __name__ == "__main__":

    print("=" * 60)
    print("MISSION MEMORY TEST")
    print("=" * 60)

    sample_mission = {
        "battery": 18,
        "wind_speed": 20,
        "gps_status": True
    }

    save_mission(
        sample_mission,
        "RETURN_TO_HOME",
        "HIGH",
        "Drone returned to home."
    )

    history = get_mission_history()

    print(f"\nStored missions: {len(history)}")

    for mission in history:
        print("\n--- Mission ---")
        print(mission)