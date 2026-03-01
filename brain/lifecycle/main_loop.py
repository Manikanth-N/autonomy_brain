import time
from models.states import TopLevelState, SubState
from models.transition_request import TransitionRequest

class MainLoop:
    def __init__(self, event_queue, safety, system_manager, controller_manager, state_machine,mission_manager):
        self.event_queue = event_queue
        self.safety = safety
        self.system_manager = system_manager
        self.controller_manager = controller_manager
        self.state_machine = state_machine
        self.mission_manager = mission_manager

        self.running = True
        self._boot_transition_done = False
        self._illegal_test_done = False

    def run(self):
        loop_rate = 20
        dt = 1.0 / loop_rate

        while self.running:
            start = time.time()

            # 1. Boot transition (only once)
            if not self._boot_transition_done:
                tr = TransitionRequest(
                    source="System",
                    target_top=TopLevelState.GROUND,
                    target_sub=SubState.STANDBY,
                    reason="BootComplete"
                )
                self.system_manager.request_transition(tr)
                self._boot_transition_done = True

            # 2. Safety evaluation
            self.safety.evaluate()

            # 3. Execute pending transition
            self.system_manager.evaluate()

            # 4. Mission logic (may request new transitions)
            self.mission_manager.update()

            # 5. Execute mission-requested transition
            self.system_manager.evaluate()

            # 6. Controller update
            state = self.state_machine.get_state()
            print("Current State:", state)
            self.controller_manager.update(state)

            elapsed = time.time() - start
            sleep_time = dt - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)