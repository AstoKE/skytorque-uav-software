from mavlink_bridge.px4_interface import PX4Interface
import time


def main():
    px4 = PX4Interface()
    px4.connect()

    print("Disarm öncesi:")
    print(px4.read_heartbeat_status())

    px4.disarm()
    time.sleep(2)

    print("Disarm sonrası:")
    print(px4.read_heartbeat_status())


if __name__ == "__main__":
    main()