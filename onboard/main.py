import time
from mavlink_bridge.px4_interface import PX4Interface
from mission_manager.state_machine import MissionStateMachine


def generate_lawnmower_pattern(width, height, lane_spacing, altitude):
    waypoints = []
    y = 0.0
    direction = 1

    while y <= height:
        if direction == 1:
            waypoints.append((0.0, y, -altitude))
            waypoints.append((width, y, -altitude))
        else:
            waypoints.append((width, y, -altitude))
            waypoints.append((0.0, y, -altitude))

        y += lane_spacing
        direction *= -1

    return waypoints


def main():
    px4 = PX4Interface("udpin:0.0.0.0:14540")
    px4.connect()

    waypoints = generate_lawnmower_pattern(
        width=5.0,
        height=6.0,
        lane_spacing=2.0,
        altitude=3.0
    )

    print("[MAIN] Oluşturulan waypointler:")
    for i, wp in enumerate(waypoints, 1):
        print(f"{i}: {wp}")

    mission = MissionStateMachine(
        px4_interface=px4,
        target_altitude=3.0,
        hold_time=5.0,
        waypoints=waypoints
    )

    while True:
        running = mission.update()
        if not running:
            break
        time.sleep(0.05)


if __name__ == "__main__":
    main()