import math
import time

import mujoco
import mujoco.viewer

from simulation.fusion.dead_reckoning import DeadReckoning
from simulation.fusion.experiment import Experiment
from simulation.fusion.plot import LivePlot, SpeedPlot
from simulation.fusion.trail import Trail
from simulation.fusion.utils import wrap_angle

exp = Experiment()
sim = exp.sim

with mujoco.viewer.launch_passive(sim.model, sim.data, show_left_ui=False, show_right_ui=False) as viewer:
    base = mujoco.mj_name2id(sim.model, mujoco.mjtObj.mjOBJ_BODY, "base")
    viewer.cam.type = mujoco.mjtCamera.mjCAMERA_TRACKING
    viewer.cam.trackbodyid = base
    viewer.cam.distance = 1.5

    trail, live, speeds, dr = Trail(
        viewer), LivePlot(), SpeedPlot(), DeadReckoning()
    n = 0

    while viewer.is_running() and sim.data.time < 60.0:
        s = exp.tick()
        trail.update(s["t"], s["x"], s["y"])

        if s["gps"] is not None:
            live.add_gps(*s["gps"])

        speeds.update(s["t"], s["v"], s["v_odo"], s["w"], s["w_gyro"])
        dr.update(s["v_odo"], s["w_gyro"], exp.dt)

        if n % 50 == 0:  # once per second
            print(f"t={s['t']:2.0f}  pos err={math.hypot(dr.x - s['x'], dr.y - s['y']):.2f} m  "
                  f"yaw err={wrap_angle(dr.yaw - s['yaw']):.3f} rad")

        n += 1
        if n % 5 == 0:  # every 0.1 s
            live.add_dr(dr.x, dr.y)
            live.update(s["x"], s["y"])

        viewer.sync()
        time.sleep(exp.dt)
