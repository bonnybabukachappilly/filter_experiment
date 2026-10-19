"""Turns a body command (v, w) into wheel speeds."""
from simulation.fusion.utils import TRACK, WHEEL_R

MAX_WHEEL = 30.0  # rad/s, ctrlrange in actuators.xml


class Controller:
    def __init__(self):
        self.v = 0.0
        self.w = 0.0

    def set_command(self, v, w):
        """Command from outside: forward speed v [m/s], yaw rate w [rad/s]."""
        self.v = v
        self.w = w

    def wheel_speeds(self):
        """Inverse unicycle: wl = (v - w*TRACK/2) / R, wr = (v + w*TRACK/2) / R."""
        wl = (self.v - self.w * TRACK / 2) / WHEEL_R
        wr = (self.v + self.w * TRACK / 2) / WHEEL_R
        return self._clip(wl), self._clip(wr)

    def _clip(self, speed):
        return max(-MAX_WHEEL, min(MAX_WHEEL, speed))
