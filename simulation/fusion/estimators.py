"""All estimators share one interface: update(s, dt) -> sets .x, .y"""
import math

from simulation.filters.dead_reckoning import DeadReckoning
from simulation.filters.kalman_filter import KF1D
from simulation.fusion.prediction import unicycle_rollout


class DeadReckoningEst:
    def __init__(self):
        self.dr = DeadReckoning()
        self.v = self.w = 0.0

    def update(self, s, dt):
        self.dr.update(s["v_odo"], s["w_gyro"], dt)
        self.v, self.w = s["v_odo"], s["w_gyro"]

    def predict_path(self, horizon=3.0):
        return unicycle_rollout(
            self.dr.x, self.dr.y, self.dr.yaw,
            self.v, self.w, horizon)

    @property
    def x(self): return self.dr.x

    @property
    def y(self): return self.dr.y


class KF1DXY:
    """Day 2: two independent scalar KFs, one for x and one for y.
    Stationary model (x = x + 0), so the real motion is treated as process noise."""

    def __init__(self, sigma_gps=2.0, q_rate=0.25):
        self.R = sigma_gps ** 2
        self.q_rate = q_rate        # m^2 per second of unmodelled motion
        self.kx = self.ky = None
        self.x = self.y = math.nan  # nan until the first GPS fix

    def update(self, s, dt):
        gps = s["gps"]
        if self.kx is None:         # initialise on the first fix
            if gps is None:
                return
            self.kx = KF1D(gps[0], self.R, 0.0, self.R)
            self.ky = KF1D(gps[1], self.R, 0.0, self.R)
        else:
            for kf in (self.kx, self.ky):
                kf.Q = self.q_rate * dt   # per-step Q scales with dt
                kf.predict(0.0)
            if gps is not None:
                self.kx.update(gps[0])
                self.ky.update(gps[1])
        self.x, self.y = self.kx.x, self.ky.x


def make_estimators():
    """Add a line here for every new filter."""
    return {
        "dead reckoning": DeadReckoningEst(),
        "KF1D (x,y)": KF1DXY(),
    }
