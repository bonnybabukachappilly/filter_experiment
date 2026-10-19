"""Fake sensors built from TRUE velocity."""
import numpy as np


class Odometry:
    """Model: v_odo = scale * v_true + noise, noise ~ N(0, sigma^2)."""

    def __init__(self, scale=1.03, sigma=0.02, seed=0):
        self.scale = scale
        self.sigma = sigma
        self.rng = np.random.default_rng(seed)

    def measure(self, v_true):
        return self.scale * v_true + self.rng.normal(0.0, self.sigma)


class Gyro:
    """w_gyro = w_true + bias + noise.
    Bias is a random walk: bias_next = bias + N(0, (walk * sqrt(dt))^2)."""

    def __init__(self, dt, sigma=0.01, walk=0.002, bias0=0.02, seed=1):
        self.dt = dt
        self.sigma = sigma
        self.walk = walk
        self.bias = bias0
        self.rng = np.random.default_rng(seed)

    def measure(self, w_true):
        self.bias += self.rng.normal(0.0, self.walk * np.sqrt(self.dt))
        return w_true + self.bias + self.rng.normal(0.0, self.sigma)


class Gps:
    """z = [x, y] + N(0, sigma^2) at `rate` Hz. Returns None when no fix."""

    def __init__(self, sigma=2.0, rate=1.0, outage=(25.0, 35.0), seed=2):
        self.sigma = sigma
        self.period = 1.0 / rate
        self.outage = outage
        self.next_time = 0.0
        self.rng = np.random.default_rng(seed)

    def measure(self, t, x, y):
        if t < self.next_time:
            return None
        self.next_time += self.period
        if self.outage[0] <= t < self.outage[1]:
            return None
        noise = self.rng.normal(0.0, self.sigma, 2)
        return x + noise[0], y + noise[1]
