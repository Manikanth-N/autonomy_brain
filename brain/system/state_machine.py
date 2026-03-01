from models.states import TopLevelState, SubState


class StateMachine:
    def __init__(self):
        self.top_state = TopLevelState.GROUND
        self.sub_state = SubState.INIT

    def set_state(self, top, sub):
        self.top_state = top
        self.sub_state = sub

    def get_state(self):
        return self.top_state, self.sub_state