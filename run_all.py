"""Headless run: simulate, run all estimators, save CSV + plots. Run: pixi run run-all"""
import os

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from simulation.fusion.estimators import make_estimators
from simulation.fusion.experiment import DURATION, Experiment

matplotlib.use("Agg")


def simulate():
    exp = Experiment()
    ests = make_estimators()
    out = {k: [] for k in ("t", "x", "y", "gps_x", "gps_y")}
    for k in ests:
        out[f"{k}|x"], out[f"{k}|y"] = [], []
    while exp.sim.data.time < DURATION:
        s = exp.tick()
        gx, gy = s["gps"] if s["gps"] is not None else (np.nan, np.nan)
        for k, v in zip(("t", "x", "y", "gps_x", "gps_y"), (s["t"], s["x"], s["y"], gx, gy)):
            out[k].append(v)
        for k, e in ests.items():
            e.update(s, exp.dt)
            out[f"{k}|x"].append(e.x)
            out[f"{k}|y"].append(e.y)
    return {k: np.array(v) for k, v in out.items()}, list(ests)


def main():
    os.makedirs("data", exist_ok=True)
    os.makedirs("results", exist_ok=True)
    d, names = simulate()
    keys = list(d)
    np.savetxt("data/sim_run.csv", np.column_stack([d[k] for k in keys]),
               delimiter=",", header=",".join(keys), comments="")

    fig, ax = plt.subplots()
    ax.plot(d["x"], d["y"], "k", label="truth")
    ax.plot(d["gps_x"], d["gps_y"], "r.", alpha=0.5, label="gps")
    for n in names:
        ax.plot(d[f"{n}|x"], d[f"{n}|y"], "--", label=n)
    ax.set_aspect("equal")
    ax.grid(True)
    ax.legend()
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    fig.savefig("results/trajectory_overlay.png", dpi=150)

    fig, ax = plt.subplots()
    print("RMSE position error:")
    for n in names:
        err = np.hypot(d[f"{n}|x"] - d["x"], d[f"{n}|y"] - d["y"])
        ax.plot(d["t"], err, label=n)
        print(f"  {n:<16} {np.sqrt(np.nanmean(err**2)):.2f} m")
    ax.axvspan(25, 35, color="gray", alpha=0.2, label="GPS outage")
    ax.set_xlabel("t [s]")
    ax.set_ylabel("position error [m]")
    ax.grid(True)
    ax.legend()
    fig.savefig("results/error_vs_time.png", dpi=150)


if __name__ == "__main__":
    main()
