from models.states import TopLevelState, SubState
from models.transition_request import TransitionRequest


class SafetySupervisor:
    def __init__(self, flags, system_manager):
        self.flags = flags
        self.system_manager = system_manager

    def evaluate(self):
        if self.flags.battery_percentage < 20:
            tr = TransitionRequest(
                source="Safety",
                target_top=TopLevelState.EMERGENCY,
                target_sub=SubState.EMERGENCY_LAND,
                reason="BatteryCritical",
            )
            self.system_manager.request_transition(tr)