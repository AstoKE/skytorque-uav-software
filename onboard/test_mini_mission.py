import time
from mavlink_bridge.px4_interface import PX4Interface


def wait_and_print_altitude(px4, duration=10):
    start = time.time()
    while time.time() - start < duration:
        alt = px4.get_relative_altitude(timeout=2)
        if alt is not None:
            print(f"Relative altitude: {alt:.2f} m")
        time.sleep(0.5)


def main():
    px4 = PX4Interface()
    px4.connect()

    print("1) Başlangıç heartbeat:")
    print(px4.read_heartbeat_status())

    print("2) Arm")
    px4.arm()
    time.sleep(2)
    print(px4.read_heartbeat_status())

    print("3) Takeoff")
    px4.takeoff(3.0)
    wait_and_print_altitude(px4, duration=12)

    print("4) Hold / Bekleme")
    time.sleep(5)

    print("5) Land")
    px4.land()
    wait_and_print_altitude(px4, duration=12)

    print("Görev tamamlandı.")


if __name__ == "__main__":
    main()