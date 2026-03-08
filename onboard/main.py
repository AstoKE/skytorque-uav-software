import time
from mavlink_bridge.px4_interface import PX4Interface
from mission_manager.state_machine import MissionStateMachine


def main():
    px4 = PX4Interface("udpin:0.0.0.0:14540")
    px4.connect()

    mission = MissionStateMachine(
        px4_interface=px4,
        target_altitude=3.0,
        hold_time=5.0,
        waypoints=[
            (3.0, 0.0, -3.0),
            (3.0, 3.0, -3.0),
            (0.0, 3.0, -3.0),
        ]
    )

    running = True
    while running:
        running = mission.update()
        time.sleep(0.05)
        

if __name__ == "__main__":
    main()