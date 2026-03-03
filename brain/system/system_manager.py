from infrastructure.logger import logger

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

        logger.info(
            f"Transition attempt: {tr.target_top} - {tr.target_sub} | Reason: {tr.reason}"
        )

        success = self.state_machine.set_state(tr.target_top, tr.target_sub)

        if success:
            logger.info(
                f"Transition SUCCESS: {tr.target_top} - {tr.target_sub}"
            )
        else:
            logger.warning(
                f"Transition BLOCKED: {tr.target_top} - {tr.target_sub}"
            )