from infrastructure.logger import logger
from brain.system.guards import TransitionGuards

class SystemManager:
    def __init__(self, state_machine, flags):
        self.state_machine = state_machine
        self.flags = flags
        self._pending_transition = None

    def request_transition(self, transition_request):
        logger.info(f"Transition requested: {transition_request}")
        self._pending_transition = transition_request

    def evaluate(self):
        if self._pending_transition:
            self._execute_transition()
            self._pending_transition = None

    
    def _execute_transition(self):
        tr = self._pending_transition

        current_top, current_sub = self.state_machine.get_state()

        if not TransitionGuards.is_allowed(
            current_top,
            current_sub,
            tr.target_top,
            tr.target_sub,
        ):
            logger.warning(
                f"Illegal transition blocked: {current_sub} → {tr.target_sub}"
            )
            return

        logger.info(
            f"Transitioning to {tr.target_top} - {tr.target_sub} | Reason: {tr.reason}"
        )

        self.state_machine.set_state(tr.target_top, tr.target_sub)