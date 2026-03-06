from pymavlink import mavutil

print("PX4 bağlantısı bekleniyor...")

master = mavutil.mavlink_connection("udpin:127.0.0.1:14540")

hb = master.recv_match(type="HEARTBEAT", blocking=True, timeout=10)

if hb is None:
    print("Heartbeat alınamadı!")
    exit(1)

system_id = hb.get_srcSystem()
component_id = hb.get_srcComponent()

master.target_system = system_id
master.target_component = component_id

print(f"Bağlantı kuruldu! system={system_id}, component={component_id}")
print("Telemetri bekleniyor...")

while True:
    msg = master.recv_match(
        type=["LOCAL_POSITION_NED", "ATTITUDE", "ALTITUDE", "BATTERY_STATUS"],
        blocking=True,
        timeout=5
    )

    if msg is None:
        print("Timeout - veri gelmedi")
        continue

    msg_type = msg.get_type()

    if msg_type == "LOCAL_POSITION_NED":
        print(f"[LOCAL_POSITION_NED] x={msg.x:.2f}, y={msg.y:.2f}, z={msg.z:.2f}")

    elif msg_type == "ATTITUDE":
        print(f"[ATTITUDE] roll={msg.roll:.3f}, pitch={msg.pitch:.3f}, yaw={msg.yaw:.3f}")

    elif msg_type == "ALTITUDE":
        print(f"[ALTITUDE] relative={msg.altitude_relative:.2f} m")

    elif msg_type == "BATTERY_STATUS":
        print(f"[BATTERY] remaining={msg.battery_remaining}%")