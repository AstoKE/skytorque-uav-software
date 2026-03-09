from typing import List, Tuple

Waypoint = Tuple[float, float, float]


def generate_lawnmower_pattern(
    width: float,
    height: float,
    lane_spacing: float,
    altitude: float,
    start_x: float = 0.0,
    start_y: float = 0.0
) -> List[Waypoint]:
    """
    LOCAL_NED koordinat sisteminde lawnmower pattern üretir.
    z değeri NED olduğu için yukarıda kalmak adına negatif verilir.
    """

    if width <= 0 or height <= 0:
        raise ValueError("width ve height pozitif olmalı")

    if lane_spacing <= 0:
        raise ValueError("lane_spacing pozitif olmalı")

    z = -abs(altitude)

    waypoints: List[Waypoint] = []
    current_y = start_y
    direction_forward = True

    while current_y <= start_y + height + 1e-6:
        if direction_forward:
            waypoints.append((start_x, current_y, z))
            waypoints.append((start_x + width, current_y, z))
        else:
            waypoints.append((start_x + width, current_y, z))
            waypoints.append((start_x, current_y, z))

        current_y += lane_spacing
        direction_forward = not direction_forward

    return waypoints