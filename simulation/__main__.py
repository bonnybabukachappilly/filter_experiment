import math
import time

import mujoco
import mujoco.viewer

from simulation.fusion.estimators import make_estimators
from simulation.fusion.experiment import DURATION, Experiment
from simulation.fusion.plot import LivePlot, SpeedPlot
from simulation.fusion.trail import Trail

exp = Experiment()
sim = exp.sim
ests = make_estimators()

with mujoco.viewer.launch_passive(sim.model, sim.data, show_left_ui=False, show_right_ui=False) as viewer:
    base = mujoco.mj_name2id(  # type: ignore
        sim.model, mujoco.mjtObj.mjOBJ_BODY, "base")  # type: ignore
    viewer.cam.type = mujoco.mjtCamera.mjCAMERA_TRACKING  # type: ignore
    viewer.cam.trackbodyid = base
    viewer.cam.distance = 1.5

    trail, live, speeds = Trail(viewer), LivePlot(list(ests)), SpeedPlot()
    n = 0

    while viewer.is_running() and sim.data.time < DURATION:
        s = exp.tick()
        trail.update(s["t"], s["x"], s["y"])

        if s["gps"] is not None:
            live.add_gps(*s["gps"])

        speeds.update(s["t"], s["v"], s["v_odo"], s["w"], s["w_gyro"])
        for e in ests.values():
            e.update(s, exp.dt)

        if n % 50 == 0:  # once per second
            errs = "  ".join(f"{k}={math.hypot(e.x - s['x'], e.y - s['y']):.2f}"
                             for k, e in ests.items())
            print(f"t={s['t']:2.0f}  pos err [m]: {errs}")

        n += 1
        if n % 5 == 0:  # every 0.1 s
            for k, e in ests.items():
                live.add_est(k, e.x, e.y)
                if hasattr(e, "predict_path"):
                    live.set_pred(k, *e.predict_path(3.0))
            live.update(s["x"], s["y"])

        viewer.sync()
        time.sleep(exp.dt)
