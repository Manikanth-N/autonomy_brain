from models.states import TopLevelState, SubState


class TransitionGuards:

    @staticmethod
    def is_allowed(current_top, current_sub, target_top, target_sub):

        # Emergency override always allowed
        if target_top == TopLevelState.EMERGENCY:
            return True

        # Define allowed transitions
        allowed = {
            SubState.INIT: [SubState.STANDBY],
            SubState.STANDBY: [SubState.ARMING],
            SubState.ARMING: [SubState.TAKEOFF],
            SubState.TAKEOFF: [SubState.MISSION],
            SubState.MISSION: [SubState.LANDING],
            SubState.LANDING: [],
            SubState.EMERGENCY_LAND: []
        }

        if current_sub in allowed:
            return target_sub in allowed[current_sub]

        return False