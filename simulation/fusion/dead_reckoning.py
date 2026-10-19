"""Dead reckoning with the unicycle model (Euler integration):
x += v cos(yaw) dt,  y += v sin(yaw) dt,  yaw += w dt."""
import math


class DeadReckoning:
    def __init__(self, x=0.0, y=0.0, yaw=0.0):
        self.x = x
        self.y = y
        self.yaw = yaw

    def update(self, v, w, dt):
        self.x += v * math.cos(self.yaw) * dt
        self.y += v * math.sin(self.yaw) * dt
        self.yaw += w * dt
