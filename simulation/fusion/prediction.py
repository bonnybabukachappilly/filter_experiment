"""Roll a state forward in time with no measurements (predict-only)."""
import math

import numpy as np


def unicycle_rollout(x, y, yaw, v, w, horizon=3.0, dt=0.1):
    """Return (xs, ys) of the predicted path. Works on local copies,
    so the real estimator is never modified."""
    n = int(horizon / dt)
    xs, ys = np.empty(n + 1), np.empty(n + 1)
    xs[0], ys[0] = x, y
    for i in range(n):
        x += v * math.cos(yaw) * dt
        y += v * math.sin(yaw) * dt
        yaw += w * dt
        xs[i + 1], ys[i + 1] = x, y
    return xs, ys
