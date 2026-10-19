"""Dot trail drawn inside the MuJoCo viewer."""
import mujoco
import numpy as np


class Trail:
    def __init__(self, viewer, every=0.2):
        self.scn = viewer.user_scn  # extra shapes drawn on top of the model
        self.every = every
        self.next_time = 0.0

    def update(self, t, x, y):
        """Drop a small red sphere at (x, y) every `every` seconds."""
        if t < self.next_time or self.scn.ngeom >= self.scn.maxgeom:
            return
        self.next_time = t + self.every
        mujoco.mjv_initGeom(
            self.scn.geoms[self.scn.ngeom], mujoco.mjtGeom.mjGEOM_SPHERE,
            np.array([0.012, 0, 0]), np.array([x, y, 0.005]),
            np.eye(3).flatten(), np.array([1, 0, 0, 1], dtype=np.float32))
        self.scn.ngeom += 1
