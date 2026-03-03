import time
from models.states import TopLevelState, SubState
from models.transition_request import TransitionRequest


class StateTimeoutSupervisor:
    def __init__(self, state_machine, system_manager):
        self.state_machine = state_machine
        self.system_manager = system_manager

        self.state_entry_time = time.time()
        self.last_state = state_machine.get_state()

        # Timeouts in seconds
        self.timeouts = {
            SubState.ARMING: 8,
            SubState.TAKEOFF: 15,
        }

    def update(self):
        current_state = self.state_machine.get_state()

        # Detect state change
        if current_state != self.last_state:
            self.state_entry_time = time.time()
            self.last_state = current_state
            return

        top, sub = current_state

        if sub in self.timeouts:
            duration = time.time() - self.state_entry_time

            if duration > self.timeouts[sub]:
                print(f"⏱ State timeout: {sub}")

                tr = TransitionRequest(
                    source="TimeoutSupervisor",
                    target_top=TopLevelState.EMERGENCY,
                    target_sub=SubState.RTL,
                    reason=f"{sub.name}Timeout"
                )

                self.system_manager.request_transition(tr)