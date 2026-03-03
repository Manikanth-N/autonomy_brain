from enum import Enum, auto


class TopLevelState(Enum):
    GROUND = auto()
    AIRBORNE = auto()
    EMERGENCY = auto()


class SubState(Enum):
    INIT = auto()
    STANDBY = auto()
    ARMING = auto()
    TAKEOFF = auto()
    MISSION = auto()
    LANDING = auto()
    RTL = auto()
    EMERGENCY_LAND = auto()