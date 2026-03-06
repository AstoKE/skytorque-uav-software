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

print("Bağlantı kuruldu!")
print(f"Heartbeat from system={system_id}, component={component_id}")
print("Mesajlar bekleniyor...")

for i in range(20):
    msg = master.recv_match(blocking=True, timeout=3)

    if msg is None:
        print("Timeout - mesaj gelmedi")
        continue

    print(msg.get_type())