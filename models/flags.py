from dataclasses import dataclass


@dataclass
class SystemFlags:
    vehicle_connected: bool = False
    battery_percentage: float = 100.0
    gps_healthy: bool = False
    armed: bool = False