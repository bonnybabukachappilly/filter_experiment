"""One simulation tick: command, physics, truth, fake sensors."""
import math

from simulation.fusion.controller import Controller
from simulation.fusion.sensors import Gps, Gyro, Odometry
from simulation.fusion.simulator import Simulator

STEPS_PER_TICK = 10  # physics steps per tick


class Experiment:
    def __init__(self):
        self.sim = Simulator()
        self.ctrl = Controller()
        self.dt = STEPS_PER_TICK * self.sim.dt  # 0.02 s per tick
        self.odo, self.gyro, self.gps = Odometry(), Gyro(self.dt), Gps()
        self.sim.reset()

    def tick(self):
        """Advance one tick. Return truth and measurements as a dict."""
        self.ctrl.set_command(
            v=0.5, w=0.3 * math.cos(0.3 * self.sim.data.time))
        for _ in range(STEPS_PER_TICK):
            self.sim.step(*self.ctrl.wheel_speeds())
        t, x, y, yaw = self.sim.truth()
        v, w = self.sim.true_vel()
        return {"t": t, "x": x, "y": y, "yaw": yaw, "v": v, "w": w,
                "v_odo": self.odo.measure(v), "w_gyro": self.gyro.measure(w),
                "gps": self.gps.measure(t, x, y)}
