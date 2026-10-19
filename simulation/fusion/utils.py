"""Shared constants and small math helpers."""
import math

WHEEL_R = 0.033  # wheel radius, m (from robot.xml)
TRACK = 0.16     # wheel separation, m (2 x 0.08)
SCENE_PATH = "simulation/model/world/scene.xml"


def quat_to_yaw(w, x, y, z) -> float:
    """Yaw from quaternion: atan2(2(wz + xy), 1 - 2(y^2 + z^2))."""
    return math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))


def wrap_angle(angle) -> float:
    """Wrap an angle to (-pi, pi]. Needed later for EKF yaw errors."""
    return math.atan2(math.sin(angle), math.cos(angle))
