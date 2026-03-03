from models.states import TopLevelState, SubState
from models.transition_request import TransitionRequest


class MissionManager:
    def __init__(self, system_manager, state_machine, vehicle):
        self.system_manager = system_manager
        self.state_machine = state_machine
        self.vehicle = vehicle

        self._arming_requested = False
        self._takeoff_requested = False
        self._mission_started = False

        self.emergency_rtl_sent = False

    def handle_event(self, event):
        if event["type"] == "ARM_STATE_CHANGED":
            # We don't transition here directly.
            # update() will read vehicle.is_armed()
            pass

    def update(self):
        top, sub = self.state_machine.get_state()

        # -------------------------------------------------
        # Reset emergency latch when not in EMERGENCY
        # -------------------------------------------------
        if top != TopLevelState.EMERGENCY:
            self.emergency_rtl_sent = False
        

        # -------------------------------------------------
        # Reset emergency state when landed and disarmed
        # -------------------------------------------------
        if top == TopLevelState.EMERGENCY and sub == SubState.RTL:
            if not self.vehicle.is_armed() and self.vehicle.get_mode() != "RTL":
                tr = TransitionRequest(
                    source="Mission",
                    target_top=TopLevelState.GROUND,
                    target_sub=SubState.STANDBY,
                    reason="EmergencyRTLComplete"
                )
                self.system_manager.request_transition(tr)

        # -------------------------------------------------
        # EMERGENCY OVERRIDE
        # -------------------------------------------------
        if top == TopLevelState.EMERGENCY:

            if sub == SubState.RTL:

                current_mode = self.vehicle.get_mode()

                if current_mode != "RTL":
                    if not self.emergency_rtl_sent:
                        print("🚨 Sending RTL command")
                        self.vehicle.rtl()
                        self.emergency_rtl_sent = True
                else:
                    # Mode confirmed
                    self.emergency_rtl_sent = False

            return

        # -------------------------------------------------
        # STANDBY → ARMING (send arm once)
        # -------------------------------------------------
        if sub == SubState.STANDBY:

            # Reset downstream flags
            self._takeoff_requested = False
            self._mission_started = False

            if not self.vehicle.is_armed():

                if self.vehicle.is_armable():

                    if not self._arming_requested:
                        print("Sending ARM command")
                        self.vehicle.arm()
                        self._arming_requested = True

                else:
                    print("Vehicle not armable yet... waiting")

            else:
                # Armed confirmed → transition
                tr = TransitionRequest(
                    source="Mission",
                    target_top=TopLevelState.GROUND,
                    target_sub=SubState.ARMING,
                    reason="ArmConfirmed"
                )
                self.system_manager.request_transition(tr)

        # -------------------------------------------------
        # ARMING → TAKEOFF (send takeoff once)
        # -------------------------------------------------
        elif sub == SubState.ARMING:

            if self.vehicle.is_armed() and not self._takeoff_requested:
                print("Sending TAKEOFF command")
                self.vehicle.takeoff(10)
                self._takeoff_requested = True

                tr = TransitionRequest(
                    source="Mission",
                    target_top=TopLevelState.AIRBORNE,
                    target_sub=SubState.TAKEOFF,
                    reason="ArmedConfirmed"
                )
                self.system_manager.request_transition(tr)

        # -------------------------------------------------
        # TAKEOFF → MISSION (transition once)
        # -------------------------------------------------
        elif sub == SubState.TAKEOFF:

            if self.vehicle.get_altitude() > 9 and not self._mission_started:
                print("Mission started")
                self._mission_started = True

                tr = TransitionRequest(
                    source="Mission",
                    target_top=TopLevelState.AIRBORNE,
                    target_sub=SubState.MISSION,
                    reason="AltitudeReached"
                )
                self.system_manager.request_transition(tr)