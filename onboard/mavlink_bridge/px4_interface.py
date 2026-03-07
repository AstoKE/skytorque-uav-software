from pymavlink import mavutil


class PX4Interface:
    def __init__(self, connection_string: str = "udpin:0.0.0.0:14540"):
        self.connection_string = connection_string
        self.master = None
        self.system_id = None
        self.component_id = None

    def connect(self):
        print(f"PX4 bağlantısı kuruluyor: {self.connection_string}")

        self.master = mavutil.mavlink_connection(self.connection_string)

        hb = self.master.recv_match(type="HEARTBEAT", blocking=True, timeout=15)
        if hb is None:
            raise TimeoutError("Heartbeat alınamadı.")

        self.system_id = hb.get_srcSystem()
        self.component_id = hb.get_srcComponent()

        self.master.target_system = self.system_id
        self.master.target_component = self.component_id

        print(f"Bağlantı kuruldu! system={self.system_id}, component={self.component_id}")

    def get_message(self, msg_types=None, timeout=5):
        return self.master.recv_match(type=msg_types, blocking=True, timeout=timeout)

    def read_heartbeat_status(self):
        msg = self.get_message(msg_types=["HEARTBEAT"], timeout=3)
        if msg is None:
            return None

        armed = bool(msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED)

        return {
            "type": "HEARTBEAT",
            "armed": armed,
            "base_mode": msg.base_mode,
            "custom_mode": msg.custom_mode,
            "system_status": msg.system_status,
        }

    def read_telemetry(self):
        msg = self.get_message(
            msg_types=["LOCAL_POSITION_NED", "ATTITUDE", "ALTITUDE", "BATTERY_STATUS"],
            timeout=5
        )

        if msg is None:
            return None

        msg_type = msg.get_type()

        if msg_type == "LOCAL_POSITION_NED":
            return {"type": "LOCAL_POSITION_NED", "x": msg.x, "y": msg.y, "z": msg.z}

        if msg_type == "ATTITUDE":
            return {"type": "ATTITUDE", "roll": msg.roll, "pitch": msg.pitch, "yaw": msg.yaw}

        if msg_type == "ALTITUDE":
            return {"type": "ALTITUDE", "relative": msg.altitude_relative}

        if msg_type == "BATTERY_STATUS":
            return {"type": "BATTERY_STATUS", "remaining": msg.battery_remaining}

        return None

    def arm(self):
        print("Arm komutu gönderiliyor...")
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            1, 0, 0, 0, 0, 0, 0
        )

    def disarm(self):
        print("Disarm komutu gönderiliyor...")
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            0, 0, 0, 0, 0, 0, 0
        )

    def takeoff(self, altitude=3.0):
        print(f"Takeoff komutu gönderiliyor... hedef irtifa: {altitude} m")

        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0,
            0, 0, 0, 0,
            float('nan'), float('nan'),
            altitude
        )

    def land(self):
        print("Land komutu gönderiliyor...")

        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_NAV_LAND,
            0,
            0, 0, 0, 0, 0, 0, 0
        )

    def get_relative_altitude(self, timeout=3):
        msg = self.get_message(msg_types=["ALTITUDE"], timeout=timeout)
        if msg is None:
            return None
        return msg.altitude_relative