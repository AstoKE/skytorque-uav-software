import time
from mavlink_bridge.px4_interface import PX4Interface


def main():
    px4 = PX4Interface()
    px4.connect()

    print("Başlangıç heartbeat:")
    print(px4.read_heartbeat_status())

    px4.arm()
    time.sleep(2)

    print("Arm sonrası heartbeat:")
    print(px4.read_heartbeat_status())

    px4.takeoff(3.0)

    print("İrtifa izleniyor...")
    start_time = time.time()

    while time.time() - start_time < 15:
        alt = px4.get_relative_altitude(timeout=2)
        if alt is not None:
            print(f"Relative altitude: {alt:.2f} m")
        time.sleep(0.5)

    print("Test tamamlandı. İstersen manuel olarak QGC'den Land yapabilirsin.")


if __name__ == "__main__":
    main()