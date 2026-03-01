from models.flags import SystemFlags
from infrastructure.event_queue import EventQueue
from brain.system.state_machine import StateMachine
from brain.system.system_manager import SystemManager
from brain.safety.safety_supervisor import SafetySupervisor
from brain.control.controller_manager import ControllerManager
from brain.mission.mission_manager import MissionManager
from brain.lifecycle.main_loop import MainLoop


def main():
    flags = SystemFlags()
    event_queue = EventQueue()
    state_machine = StateMachine()
    system_manager = SystemManager(state_machine, flags)
    safety = SafetySupervisor(flags, system_manager)
    controller_manager = ControllerManager()
    mission_manager = MissionManager(system_manager, state_machine)

    loop = MainLoop(event_queue, safety, system_manager, controller_manager, state_machine,mission_manager)
    loop.run()


if __name__ == "__main__":
    main()