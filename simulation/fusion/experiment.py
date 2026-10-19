"""One simulation tick: command, physics, truth, fake sensors."""
import math
from typing import Any

from simulation.fusion.controller import Controller
from simulation.fusion.sensors import Gps, Gyro, Odometry
from simulation.fusion.simulator import Simulator

STEPS_PER_TICK = 10
DURATION = 60.0

V_CMD = 0.8
T_EIGHT = 60.0
W_MAX = 4 * math.pi / T_EIGHT


def figure8_command(t) -> tuple[float, float]:
    """Return (v, w). w flips sign every T_EIGHT/2 seconds."""
    w: float = math.copysign(W_MAX, math.sin(2 * math.pi * t / T_EIGHT))
    return V_CMD, w


class Experiment:
    def __init__(self) -> None:
        self.sim = Simulator()
        self.ctrl = Controller()
        self.dt = STEPS_PER_TICK * self.sim.dt
        self.odo, self.gyro, self.gps = Odometry(), Gyro(self.dt), Gps()
        self.sim.reset()

    def tick(self) -> dict[str, Any]:
        """Advance one tick. Return truth and measurements as a dict."""
        v_cmd, w_cmd = figure8_command(self.sim.data.time)
        self.ctrl.set_command(v=v_cmd, w=w_cmd)
        for _ in range(STEPS_PER_TICK):
            self.sim.step(*self.ctrl.wheel_speeds())
        t, x, y, yaw = self.sim.truth()
        v, w = self.sim.true_vel()
        return {"t": t, "x": x, "y": y, "yaw": yaw, "v": v, "w": w,
                "v_odo": self.odo.measure(v), "w_gyro": self.gyro.measure(w),
                "gps": self.gps.measure(t, x, y)}
