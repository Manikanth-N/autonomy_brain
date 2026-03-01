class ControllerManager:
    def __init__(self):
        self.active_controller = None

    def update(self, state):
        top, sub = state

        if sub.name == "TAKEOFF":
            self.active_controller = "TakeoffController"
        elif sub.name == "MISSION":
            self.active_controller = "MissionController"
        elif sub.name == "LANDING":
            self.active_controller = "LandingController"
        elif sub.name == "EMERGENCY_LAND":
            self.active_controller = "EmergencyController"

        print(f"Active Controller: {self.active_controller}")