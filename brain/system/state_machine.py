from models.states import TopLevelState, SubState


class StateMachine:
    def __init__(self):
        self.top_state = TopLevelState.GROUND
        self.sub_state = SubState.INIT

        self.allowed_transitions = {
            (TopLevelState.GROUND, SubState.INIT): [
                (TopLevelState.GROUND, SubState.STANDBY),
            ],

            (TopLevelState.GROUND, SubState.STANDBY): [
                (TopLevelState.GROUND, SubState.ARMING),
            ],

            (TopLevelState.GROUND, SubState.ARMING): [
                (TopLevelState.AIRBORNE, SubState.TAKEOFF),
            ],

            (TopLevelState.AIRBORNE, SubState.TAKEOFF): [
                (TopLevelState.AIRBORNE, SubState.MISSION),
            ],

            (TopLevelState.AIRBORNE, SubState.MISSION): [
                # future landing transition here
            ],
        }

    def set_state(self, target_top, target_sub):

        current = (self.top_state, self.sub_state)
        target = (target_top, target_sub)

        # 🚨 Emergency override always allowed
        if target_top == TopLevelState.EMERGENCY:
            self.top_state = target_top
            self.sub_state = target_sub
            return True

        # Check if allowed
        allowed = target in self.allowed_transitions.get(current, [])

        if not allowed:
            print(f"⚠ Illegal transition blocked: {current} → {target}")
            return False

        self.top_state = target_top
        self.sub_state = target_sub
        return True

    def get_state(self):
        return self.top_state, self.sub_state