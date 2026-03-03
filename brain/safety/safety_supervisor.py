from models.states import TopLevelState, SubState
from models.transition_request import TransitionRequest


class SafetySupervisor:
    def __init__(self, flags, system_manager):
        self.flags = flags
        self.system_manager = system_manager
        self.emergency_triggered = False

    def evaluate(self):
        if self.flags.battery_percentage < 20:
            tr = TransitionRequest(
                source="Safety",
                target_top=TopLevelState.EMERGENCY,
                target_sub=SubState.EMERGENCY_LAND,
                reason="BatteryCritical",
            )
            self.system_manager.request_transition(tr)
    
    def handle_event(self, event):
        if event["type"] == "LINK_LOST" and not self.emergency_triggered:

            self.emergency_triggered = True

            tr = TransitionRequest(
                source="Safety",
                target_top=TopLevelState.EMERGENCY,
                target_sub=SubState.RTL,
                reason="LinkLost"
            )
            self.system_manager.request_transition(tr)

        elif event["type"] == "LINK_RESTORED":
            self.emergency_triggered = False
        
        if event["type"] == "LOW_BATTERY":
            self.emergency_triggered = True
            tr = TransitionRequest(
                source="Safety",
                target_top=TopLevelState.EMERGENCY,
                target_sub=SubState.RTL,
                reason="LowBattery"
            )
            self.system_manager.request_transition(tr)