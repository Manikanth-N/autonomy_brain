from models.states import TopLevelState, SubState


class TransitionGuards:

    # Explicit full-state transition map
    ALLOWED_TRANSITIONS = {

        # GROUND PHASE
        (TopLevelState.GROUND, SubState.INIT):
            [(TopLevelState.GROUND, SubState.STANDBY)],

        (TopLevelState.GROUND, SubState.STANDBY):
            [(TopLevelState.GROUND, SubState.ARMING)],

        (TopLevelState.GROUND, SubState.ARMING):
            [(TopLevelState.AIRBORNE, SubState.TAKEOFF)],

        # AIRBORNE PHASE
        (TopLevelState.AIRBORNE, SubState.TAKEOFF):
            [(TopLevelState.AIRBORNE, SubState.MISSION)],

        (TopLevelState.AIRBORNE, SubState.MISSION):
            [(TopLevelState.AIRBORNE, SubState.LANDING)],

        (TopLevelState.AIRBORNE, SubState.LANDING):
            [(TopLevelState.GROUND, SubState.STANDBY)],

        # EMERGENCY stays in EMERGENCY
        (TopLevelState.EMERGENCY, SubState.RTL):
            [],
        
        # Allowed EMERGENCY exit (e.g. after RTL completes)
        (TopLevelState.EMERGENCY, SubState.RTL):
            [(TopLevelState.GROUND, SubState.STANDBY)]
    }


    @staticmethod
    def is_allowed(current_top, current_sub, target_top, target_sub):

        # 1️⃣ Block redundant transitions
        if (current_top, current_sub) == (target_top, target_sub):
            return False

        # 2️⃣ Emergency override always allowed
        if target_top == TopLevelState.EMERGENCY:
            return True

        # 3️⃣ Prevent leaving EMERGENCY unless explicitly allowed
        if current_top == TopLevelState.EMERGENCY and target_top != TopLevelState.EMERGENCY:
            return False
        
        allowed_targets = allowed_transitions.get(
            (current_top, current_sub),
            []
        )

        return (target_top, target_sub) in allowed_targets