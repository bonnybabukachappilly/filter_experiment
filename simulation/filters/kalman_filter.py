"""Scalar (1D) Kalman filter."""


class KF1D:
    def __init__(self, x0, P0, Q, R):
        self.x = x0      # state estimate
        self.P = P0      # estimate variance
        self.Q = Q       # process noise variance PER PREDICT STEP
        self.R = R       # measurement noise variance
        self.K = 0.0     # last gain (kept for plots)
        self.innov = 0.0  # last residual z - x (kept for Day 3 checks)
        self.S = 0.0     # last innovation variance P + R

    def predict(self, u=0.0):
        self.x = self.x + u
        self.P = self.P + self.Q

    def update(self, z):
        self.innov = z - self.x
        self.S = self.P + self.R
        self.K = self.P / self.S
        self.x = self.x + self.K * self.innov
        self.P = (1.0 - self.K) * self.P
