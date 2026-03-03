from models.states import TopLevelState, SubState
from brain.control.takeoff_controller import TakeoffController
from brain.control.mission_controller import MissionController


class ControllerManager:

    def __init__(self):
        self.takeoff_controller = TakeoffController()
        self.mission_controller = MissionController()

        self.active_controller = None

    def update(self, state):
        top, sub = state

        # EMERGENCY overrides everything
        if top == TopLevelState.EMERGENCY:
            self.active_controller = None
            return

        if sub == SubState.TAKEOFF:
            self.active_controller = self.takeoff_controller

        elif sub == SubState.MISSION:
            self.active_controller = self.mission_controller

        else:
            self.active_controller = None

        if self.active_controller:
            self.active_controller.update()