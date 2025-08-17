import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Parameters
c = 0.5
m = 1
zeta = c / m
v0 = 1

# Time span
t_end = 5.0

# Initial dt
dt0 = 0.1
time = np.arange(0, t_end + dt0, dt0)

# Exact solution
velocity_exact = v0 * np.exp(-zeta * time)

# Explicit Euler
velocity_explicit = v0 * (1 - zeta*dt0) ** np.arange(len(time))

# Implicit Euler
velocity_implicit = v0 * (1 / (1 + zeta*dt0)) ** np.arange(len(time))

# --- Plot setup ---
fig, ax = plt.subplots(figsize=(8,6))
plt.subplots_adjust(bottom=0.25)  # leave space for slider

line_exact, = ax.plot(time, velocity_exact, 'k-', label="Exact")
line_explicit, = ax.plot(time, velocity_explicit, 'r--', label="Explicit Euler")
line_implicit, = ax.plot(time, velocity_implicit, 'b-.', label="Implicit Euler")

ax.set_xlim(0, t_end)   # <<< Fix x-axis limit to 0–5 sec
ax.set_xlabel("Time (s)", fontsize=14)
ax.set_ylabel("Velocity", fontsize=14)
ax.set_title("Effect of dt on Stability (Euler Methods)", fontsize=16)
ax.legend(fontsize=12)
ax.grid(True)

# --- Slider setup ---
ax_dt = plt.axes([0.2, 0.1, 0.6, 0.03])  # x, y, width, height
dt_slider = Slider(ax_dt, 'dt', 0.01, 5.0, valinit=dt0, valstep=0.01)

# --- Update function ---
def update(val):
    dt = dt_slider.val
    time = np.arange(0, t_end + dt, dt)

    velocity_exact = v0 * np.exp(-zeta * time)
    velocity_explicit = v0 * (1 - zeta*dt) ** np.arange(len(time))
    velocity_implicit = v0 * (1 / (1 + zeta*dt)) ** np.arange(len(time))

    # update data
    line_exact.set_data(time, velocity_exact)
    line_explicit.set_data(time, velocity_explicit)
    line_implicit.set_data(time, velocity_implicit)

    # keep axis fixed to 0–5 sec
    ax.set_xlim(0, t_end)
    ax.set_ylim(min(velocity_explicit.min(), velocity_implicit.min(), velocity_exact.min())*1.1,
                max(velocity_explicit.max(), velocity_implicit.max(), velocity_exact.max())*1.1)

    fig.canvas.draw_idle()

# Connect slider to update function
dt_slider.on_changed(update)

plt.show()
