from models.states import TopLevelState, SubState
from models.transition_request import TransitionRequest


class MissionManager:
    def __init__(self, system_manager, state_machine):
        self.system_manager = system_manager
        self.state_machine = state_machine

        self._arming_requested = False
        self._takeoff_requested = False
        self._mission_started = False

    def update(self):
        top, sub = self.state_machine.get_state()

        # STANDBY → ARMING
        if sub == SubState.STANDBY and not self._arming_requested:
            tr = TransitionRequest(
                source="Mission",
                target_top=TopLevelState.GROUND,
                target_sub=SubState.ARMING,
                reason="ArmRequested"
            )
            self.system_manager.request_transition(tr)
            self._arming_requested = True

        # ARMING → TAKEOFF
        elif sub == SubState.ARMING and not self._takeoff_requested:
            tr = TransitionRequest(
                source="Vehicle",
                target_top=TopLevelState.AIRBORNE,
                target_sub=SubState.TAKEOFF,
                reason="ArmedConfirmed"
            )
            self.system_manager.request_transition(tr)
            self._takeoff_requested = True

        # TAKEOFF → MISSION
        elif sub == SubState.TAKEOFF and not self._mission_started:
            tr = TransitionRequest(
                source="Mission",
                target_top=TopLevelState.AIRBORNE,
                target_sub=SubState.MISSION,
                reason="AltitudeReached"
            )
            self.system_manager.request_transition(tr)
            self._mission_started = True