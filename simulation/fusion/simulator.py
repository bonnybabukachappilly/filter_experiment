import math

import mujoco

from simulation.fusion.utils import SCENE_PATH, quat_to_yaw


class Simulator:
    def __init__(self, scene_path=SCENE_PATH):
        self.model = mujoco.MjModel.from_xml_path(scene_path)
        self.data = mujoco.MjData(self.model)
        self.dt = self.model.opt.timestep

    def reset(self):
        mujoco.mj_resetData(self.model, self.data)

    def step(self, wl, wr):
        """Command wheel speeds [rad/s], advance one timestep."""
        self.data.ctrl[:] = [wl, wr]
        mujoco.mj_step(self.model, self.data)

    def truth(self):
        """Return (t, x, y, yaw) from the simulator state."""
        d = self.data
        return d.time, d.qpos[0], d.qpos[1], quat_to_yaw(*d.qpos[3:7])

    def true_vel(self):
        """Return (v, w): forward speed along heading, yaw rate."""
        d = self.data
        yaw = quat_to_yaw(*d.qpos[3:7])
        v = d.qvel[0] * math.cos(yaw) + d.qvel[1] * math.sin(yaw)
        return v, d.qvel[5]
