"""Quick environment + simulator check. Run: pixi run smoke"""
import numpy as np


def main():
    import filterpy.kalman  # noqa: F401  (fails here if NumPy/SciPy clash)

    from simulation.fusion.experiment import Experiment

    exp = Experiment()
    for _ in range(100):
        s = exp.tick()

    keys = ("x", "y", "yaw", "v", "w", "v_odo", "w_gyro")
    assert all(np.isfinite(s[k]) for k in keys), "non-finite value in sim"
    print(
        f"OK  t={s['t']:.2f}s  x={s['x']:.3f}  y={s['y']:.3f}  v={s['v']:.3f} m/s")


if __name__ == "__main__":
    main()
