"""Plotting helpers."""
import matplotlib.pyplot as plt


class Plotter:
    def __init__(self):
        self.fig, self.ax = plt.subplots()

    def add_path(self, xs, ys, label):
        self.ax.plot(xs, ys, label=label)

    def show(self):
        self.ax.set_aspect("equal")  # 1 m looks the same on both axes
        self.ax.set_xlabel("x [m]")
        self.ax.set_ylabel("y [m]")
        self.ax.grid(True)
        self.ax.legend()
        plt.show()


class LivePlot:
    def __init__(self):
        plt.ion()  # interactive mode: the window updates without blocking
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], label="truth")
        self.gps_line, = self.ax.plot([], [], "r.", label="gps")
        self.dr_line, = self.ax.plot([], [], "g--", label="dead reckoning")
        self.dx, self.dy = [], []
        self.gx, self.gy = [], []
        self.ax.legend()
        self.xs, self.ys = [], []
        self.ax.set_aspect("equal", adjustable="datalim")
        self.ax.set_xlabel("x [m]")
        self.ax.set_ylabel("y [m]")
        self.ax.grid(True)

    def update(self, x, y):
        self.xs.append(x)
        self.ys.append(y)
        self.line.set_data(self.xs, self.ys)
        self.ax.relim()
        self.ax.autoscale_view()
        plt.pause(0.001)  # let the window redraw

    def add_gps(self, x, y):
        self.gx.append(x)
        self.gy.append(y)
        self.gps_line.set_data(self.gx, self.gy)

    def add_dr(self, x, y):
        self.dx.append(x)
        self.dy.append(y)
        self.dr_line.set_data(self.dx, self.dy)


class SpeedPlot:
    """Top: forward speed v. Bottom: yaw rate w. Truth vs sensor."""

    def __init__(self):
        self.fig, (self.av, self.aw) = plt.subplots(2, 1, sharex=True)
        self.d = [[] for _ in range(5)]  # t, v_true, v_odo, w_true, w_gyro
        self.lines = [
            self.av.plot([], [], "k-", label="true v")[0],
            self.av.plot([], [], "c-", alpha=0.6, label="odometry v")[0],
            self.aw.plot([], [], "k-", label="true w")[0],
            self.aw.plot([], [], "m-", alpha=0.6, label="gyro w")[0],
        ]
        self.av.set_ylabel("v [m/s]")
        self.aw.set_ylabel("w [rad/s]")
        self.aw.set_xlabel("t [s]")
        self.av.legend()
        self.aw.legend()

    def update(self, t, v, v_odo, w, w_gyro):
        for lst, val in zip(self.d, (t, v, v_odo, w, w_gyro)):
            lst.append(val)
        for line, ydata in zip(self.lines, self.d[1:]):
            line.set_data(self.d[0], ydata)
        for ax in (self.av, self.aw):
            ax.relim()
            ax.autoscale_view()
