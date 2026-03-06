from pymavlink import mavutil

print("PX4 bağlantısı bekleniyor...")

master = mavutil.mavlink_connection("udpin:127.0.0.1:14540")
msg = master.wait_heartbeat(timeout=10)

print("Bağlantı kuruldu!")
print(f"Heartbeat System ID: {msg.get_srcSystem()}")
print(f"Heartbeat Component ID: {msg.get_srcComponent()}")