import numpy, scipy, matplotlib, pandas, mujoco, filterpy, ahrs
print("numpy", numpy.__version__)
print("mujoco", mujoco.__version__)

m = mujoco.MjModel.from_xml_string("""
<mujoco><worldbody><body><joint type="free"/><geom size=".1"/></body></worldbody></mujoco>
""")
d = mujoco.MjData(m)
mujoco.mj_step(m, d)
print("MuJoCo step OK")
