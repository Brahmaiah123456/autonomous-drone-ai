class DroneSimulator:
    """
    Simulated drone used for testing the autonomous
    mission intelligence system.

    No real drone hardware is required.
    """

    def __init__(
        self,
        battery=100,
        wind_speed=10,
        gps_status=True
    ):
        self.battery = battery
        self.wind_speed = wind_speed
        self.gps_status = gps_status
        self.mission_active = False

    # ------------------------------------------------
    # SENSOR TOOLS
    # ------------------------------------------------

    def get_battery(self):
        return self.battery

    def get_weather(self):
        return self.wind_speed

    def get_gps_status(self):
        return self.gps_status

    # ------------------------------------------------
    # DRONE ACTIONS
    # ------------------------------------------------

    def start_mission(self):

        if self.battery < 30:
            return {
                "success": False,
                "message": (
                    "Mission blocked: "
                    "battery is below 30%."
                )
            }

        if self.wind_speed > 30:
            return {
                "success": False,
                "message": (
                    "Mission blocked: "
                    "wind speed is unsafe."
                )
            }

        if not self.gps_status:
            return {
                "success": False,
                "message": (
                    "Mission blocked: "
                    "GPS is unavailable."
                )
            }

        self.mission_active = True

        return {
            "success": True,
            "message": "Mission started successfully."
        }

    def return_to_home(self):

        self.mission_active = False

        return {
            "success": True,
            "action": "RETURN_TO_HOME",
            "message": (
                "Drone is returning to the home location."
            )
        }

    def abort_mission(self):

        self.mission_active = False

        return {
            "success": True,
            "action": "ABORT_MISSION",
            "message": (
                "Mission aborted. "
                "Drone will perform a safe landing."
            )
        }

    def pause_mission(self):

        self.mission_active = False

        return {
            "success": True,
            "action": "PAUSE_MISSION",
            "message": "Mission paused for safety."
        }

    # ------------------------------------------------
    # SIMULATE BATTERY CHANGE
    # ------------------------------------------------

    def consume_battery(self, amount):

        self.battery -= amount

        if self.battery < 0:
            self.battery = 0

        return self.battery


# ====================================================
# TEST
# ====================================================

if __name__ == "__main__":

    print("=" * 60)
    print("DRONE SIMULATOR TEST")
    print("=" * 60)

    drone = DroneSimulator(
        battery=18,
        wind_speed=20,
        gps_status=True
    )

    print(
        f"\nBattery: "
        f"{drone.get_battery()}%"
    )

    print(
        f"Wind speed: "
        f"{drone.get_weather()} km/h"
    )

    print(
        f"GPS available: "
        f"{drone.get_gps_status()}"
    )

    print("\nTrying to start mission...")

    result = drone.start_mission()

    print(result)

    print("\nExecuting Return-to-Home...")

    result = drone.return_to_home()

    print(result)

    print("\n" + "=" * 60)
    print("SIMULATOR TEST COMPLETE")
    print("=" * 60)