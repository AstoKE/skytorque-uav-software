from mavlink_bridge.px4_interface import PX4Interface


def main():
    px4 = PX4Interface("udpin:127.0.0.1:14540")
    px4.connect()

    print("Heartbeat durumu:")
    for _ in range(3):
        print(px4.read_heartbeat_status())

    print("Telemetri okunuyor...")
    while True:
        telemetry = px4.read_telemetry()
        if telemetry is not None:
            print(telemetry)


if __name__ == "__main__":
    main()