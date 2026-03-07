from mavlink_bridge.px4_interface import PX4Interface


def main():
    px4 = PX4Interface()
    px4.connect()

    print("Heartbeat:")
    for _ in range(3):
        print(px4.read_heartbeat_status())

    print("Telemetri:")
    for _ in range(10):
        msg = px4.read_telemetry()
        if msg:
            print(msg)


if __name__ == "__main__":
    main()