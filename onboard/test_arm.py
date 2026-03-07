import time
from mavlink_bridge.px4_interface import PX4Interface


def main():
    px4 = PX4Interface()
    px4.connect()

    print("Arm öncesi:")
    print(px4.read_heartbeat_status())

    px4.arm()
    time.sleep(2)

    print("Arm sonrası heartbeat:")
    for _ in range(5):
        hb = px4.read_heartbeat_status()
        if hb is not None:
            print(hb)
        time.sleep(1)


if __name__ == "__main__":
    main()