import time
from enum import Enum


class MissionState(Enum):
    INIT = "INIT"
    ARMING = "ARMING"
    TAKEOFF = "TAKEOFF"
    OFFBOARD_PREP = "OFFBOARD_PREP"
    NAVIGATE = "NAVIGATE"
    HOLD = "HOLD"
    LANDING = "LANDING"
    COMPLETE = "COMPLETE"
    FAILSAFE = "FAILSAFE"


class MissionStateMachine:
    def __init__(self, px4_interface, target_altitude=3.0, hold_time=5.0, nav_target=(5.0, 0.0, -3.0)):
        self.px4 = px4_interface
        self.state = MissionState.INIT
        self.target_altitude = target_altitude
        self.hold_time = hold_time
        self.nav_target = nav_target
        self.state_start_time = time.time()

        self.takeoff_command_sent = False
        self.land_command_sent = False
        self.navigate_command_sent = False

    def set_state(self, new_state: MissionState):
        print(f"[STATE] {self.state.value} -> {new_state.value}")
        self.state = new_state
        self.state_start_time = time.time()

        if new_state == MissionState.TAKEOFF:
            self.takeoff_command_sent = False

        if new_state == MissionState.NAVIGATE:
            self.navigate_command_sent = False

        if new_state == MissionState.LANDING:
            self.land_command_sent = False

    def state_elapsed(self):
        return time.time() - self.state_start_time

    def update(self):
        try:
            if self.state == MissionState.INIT:
                self.handle_init()

            elif self.state == MissionState.ARMING:
                self.handle_arming()

            elif self.state == MissionState.TAKEOFF:
                self.handle_takeoff()

            elif self.state == MissionState.OFFBOARD_PREP:
                self.handle_offboard_prep()

            elif self.state == MissionState.HOLD:
                self.handle_hold()

            elif self.state == MissionState.NAVIGATE:
                self.handle_navigate()

            elif self.state == MissionState.LANDING:
                self.handle_landing()

            elif self.state == MissionState.COMPLETE:
                print("[MISSION] Görev tamamlandı.")
                return False

            elif self.state == MissionState.FAILSAFE:
                print("[MISSION] FAILSAFE aktif.")
                return False

            return True

        except Exception as e:
            print(f"[ERROR] State machine hatası: {e}")
            self.set_state(MissionState.FAILSAFE)
            return True

    def handle_init(self):
        hb = self.px4.read_heartbeat_status()
        if hb is None:
            print("[INIT] Heartbeat bekleniyor...")
            return

        print(f"[INIT] Heartbeat alındı: {hb}")
        self.set_state(MissionState.ARMING)

    def handle_arming(self):
        hb = self.px4.read_heartbeat_status()
        if hb is None:
            print("[ARMING] Heartbeat alınamadı.")
            return

        if hb["armed"]:
            print("[ARMING] Araç zaten armed.")
            self.set_state(MissionState.TAKEOFF)
            return

        print("[ARMING] Arm komutu gönderiliyor...")
        self.px4.arm()
        time.sleep(2)

        hb = self.px4.read_heartbeat_status()
        if hb and hb["armed"]:
            print("[ARMING] Arm başarılı.")
            self.set_state(MissionState.TAKEOFF)
        else:
            print("[ARMING] Arm başarısız.")
            self.set_state(MissionState.FAILSAFE)

    def handle_takeoff(self):
        if not self.takeoff_command_sent:
            print(f"[TAKEOFF] {self.target_altitude} m takeoff komutu gönderiliyor...")
            self.px4.takeoff(self.target_altitude)
            self.takeoff_command_sent = True
            time.sleep(1)

        alt = self.px4.get_relative_altitude(timeout=2)
        if alt is None:
            print("[TAKEOFF] İrtifa verisi yok.")
            return

        print(f"[TAKEOFF] Mevcut irtifa: {alt:.2f} m")

        if alt >= self.target_altitude * 0.85:
            print("[TAKEOFF] Hedef irtifaya ulaşıldı.")
            self.set_state(MissionState.OFFBOARD_PREP)
            return

        if self.state_elapsed() > 20:
            print("[TAKEOFF] Timeout - hedef irtifaya ulaşılamadı.")
            self.set_state(MissionState.FAILSAFE)

    def handle_hold(self):
        alt = self.px4.get_relative_altitude(timeout=2)
        if alt is not None:
            print(f"[HOLD] İrtifa: {alt:.2f} m")

        if self.state_elapsed() >= self.hold_time:
            print("[HOLD] Bekleme tamamlandı.")
            self.set_state(MissionState.LANDING)

    def handle_landing(self):
        if not self.land_command_sent:
            print("[LANDING] Land komutu gönderiliyor...")
            self.px4.land()
            self.land_command_sent = True
            time.sleep(1)

        alt = self.px4.get_relative_altitude(timeout=2)
        if alt is None:
            print("[LANDING] İrtifa verisi yok.")
            return

        print(f"[LANDING] Mevcut irtifa: {alt:.2f} m")

        if alt <= 0.15:
            print("[LANDING] İniş tamamlandı.")
            self.set_state(MissionState.COMPLETE)
            return

        if self.state_elapsed() > 20:
            print("[LANDING] Timeout - iniş tamamlanamadı.")
            self.set_state(MissionState.FAILSAFE)

    def handle_navigate(self):
        target_x, target_y, target_z = self.nav_target

        self.px4.go_to_local_position(target_x, target_y, target_z)

        pos = self.px4.get_local_position(timeout=2)
        if pos is None:
            print("[NAVIGATE] Konum verisi yok.")
            return

        print(f"[NAVIGATE] Mevcut konum: x={pos['x']:.2f}, y={pos['y']:.2f}, z={pos['z']:.2f}")

        dx = abs(pos["x"] - target_x)
        dy = abs(pos["y"] - target_y)
        dz = abs(pos["z"] - target_z)

        if dx < 0.5 and dy < 0.5 and dz < 0.5:
            print("[NAVIGATE] Hedef noktaya ulaşıldı.")
            self.set_state(MissionState.HOLD)
            return

        if self.state_elapsed() > 20:
            print("[NAVIGATE] Timeout - hedef noktaya ulaşılamadı.")
            self.set_state(MissionState.FAILSAFE)


    def handle_offboard_prep(self):
        target_x, target_y, target_z = self.nav_target

        # PX4 OFFBOARD'a geçmeden önce setpoint akışı görmek ister
        self.px4.go_to_local_position(target_x, target_y, target_z)

        pos = self.px4.get_local_position(timeout=2)
        if pos is not None:
            print(f"[OFFBOARD_PREP] Setpoint akışı gönderiliyor... x={pos['x']:.2f}, y={pos['y']:.2f}, z={pos['z']:.2f}")

        # Yaklaşık 1 saniye setpoint aktıktan sonra OFFBOARD'a geç
        if self.state_elapsed() > 1.0:
            self.px4.set_offboard_mode()
            print("[OFFBOARD_PREP] OFFBOARD mod istendi.")
            self.set_state(MissionState.NAVIGATE)

