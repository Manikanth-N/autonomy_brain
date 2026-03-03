import threading
import time
from pymavlink import mavutil


class VehicleInterface:

    def __init__(self, connection_string, event_queue):
        self.connection_string = connection_string
        self.event_queue = event_queue

        self.master = None
        self.thread = None
        self.running = False

        self.start_time = time.time()

        # State cache
        self.connected = False
        self.armed = False
        self.mode = None
        self.altitude = 0.0
        self.last_heartbeat = 0
        self.link_lost = False
        self.battery_remaining = None
        self.system_status = None
        self.gps_fix_type = 0

    # -------------------------
    # Connection
    # -------------------------

    def connect(self):
        print("Connecting to vehicle...")
        self.master = mavutil.mavlink_connection(self.connection_string)

        self.master.wait_heartbeat()
        print("Heartbeat received")

        self.last_heartbeat = time.time()
        self.connected = True

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    # -------------------------
    # Thread Loop
    # -------------------------

    def _run(self):
        while self.running:
            msg = self.master.recv_match(blocking=False)

            if msg:
                self._handle_message(msg)

            now = time.time()

            # ---- Grace period after boot ----
            if self.connected and (now - self.start_time > 3):

                # ---- Link lost detection ----
                if (now - self.last_heartbeat > 2) and not self.link_lost:
                    self.link_lost = True
                    print("⚠ LINK LOST")
                    self.event_queue.push({"type": "LINK_LOST"})

                # ---- Link restored detection ----
                elif (now - self.last_heartbeat <= 2) and self.link_lost:
                    self.link_lost = False
                    print("✅ LINK RESTORED")
                    self.event_queue.push({"type": "LINK_RESTORED"})

            time.sleep(0.01)  # 100 Hz loop, prevents CPU spin

    # -------------------------
    # Message Handling
    # -------------------------

    def _handle_message(self, msg):
        mtype = msg.get_type()

        if mtype == "HEARTBEAT":
            self.last_heartbeat = time.time()

            self.system_status = msg.system_status

            old_armed = self.armed
            self.armed = self.master.motors_armed()
            self.mode = self.master.flightmode

            if old_armed != self.armed:
                self.event_queue.push({
                    "type": "ARM_STATE_CHANGED",
                    "armed": self.armed
                })

        elif mtype == "GLOBAL_POSITION_INT":
            self.altitude = msg.relative_alt / 1000.0
        
        elif mtype == "GPS_RAW_INT":
            self.gps_fix_type = msg.fix_type

        elif mtype == "VFR_HUD":
            self.altitude = msg.alt  # More reliable for Copter

        elif mtype == "SYS_STATUS":
            self.battery_remaining = msg.battery_remaining

            if self.battery_remaining is not None and self.battery_remaining < 20:
                self.event_queue.push({"type": "LOW_BATTERY"})



    # -------------------------
    # Public API
    # -------------------------

    def is_armed(self):
        return self.armed

    def get_mode(self):
        return self.mode

    def get_altitude(self):
        return self.altitude

    def get_battery(self):
        return self.battery_remaining

    def arm(self):
        self.master.set_mode("GUIDED")
        self.master.arducopter_arm()

    def disarm(self):
        self.master.arducopter_disarm()

    def takeoff(self, altitude):
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0,
            0, 0, 0, 0,
            0, 0,
            altitude
        )

    def rtl(self):
        self.master.set_mode_rtl()
    
    def is_armable(self):
        return (
            self.system_status == mavutil.mavlink.MAV_STATE_STANDBY
            and self.gps_fix_type >= 3
            and not self.armed
        )