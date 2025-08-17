import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Parameters
c = 0.5
m = 1
zeta = c / m
v0 = 1

# dt values for slider
dt_values = np.arange(0.1, 1, 0.01)

# initial dt
dt0 = dt_values[0]
time = np.arange(0, 5 + dt0, dt0)

# exact solution
velocity_exact = v0 * np.exp(-zeta * time)

# explicit and implicit (initiating dt)
velocity_explicit = v0 * (1 - zeta*dt0) ** np.arange(len(time))
velocity_implicit = v0 * (1 / (1 + zeta*dt0)) ** np.arange(len(time))
error_explicit=abs(velocity_exact-velocity_explicit)
error_implicit=abs(velocity_exact-velocity_implicit)
global_error_explicit=np.sqrt(np.mean(error_explicit**2))
global_error_implicit=np.sqrt(np.mean(error_implicit**2))

# --- Create figure with 2 subplots ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
plt.subplots_adjust(bottom=0.25)  # space for slider

# Plot initial curves
line_exact1, = ax1.plot(time, velocity_exact, 'r-', linewidth=2, label="Exact")
line_explicit,   = ax1.plot(time, velocity_explicit, 'o-',color='g', label=f"Explicit dt={dt0}")

line_exact2, = ax2.plot(time, velocity_exact, 'r-', linewidth=2, label="Exact")
line_implicit,   = ax2.plot(time, velocity_implicit, 'o-',color='g', label=f"Implicit dt={dt0}")

# formatting
ax1.set_title("Explicit Euler vs Exact", fontsize=14)
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Velocity")
ax1.legend()
ax1.grid(True)

ax2.set_title("Implicit Euler vs Exact", fontsize=14)
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Velocity")
ax2.legend()
ax2.grid(True)

# --- Slider ---
ax_dt = plt.axes([0.4, 0.1, 0.2, 0.03])   # position [left, bottom, width, height]
dt_slider = Slider(ax_dt, 'dt', valmin=dt_values.min(), valmax=dt_values.max(),
                   valinit=dt0, valstep=dt_values)

# --- Update function ---
def update(val):
    dt = dt_slider.val
    time = np.arange(0, 5 + dt, dt)

    # recompute curves
    velocity_exact = v0 * np.exp(-zeta * time)
    velocity_explicit = v0 * (1 - zeta*dt) ** np.arange(len(time))
    velocity_implicit = v0 * (1 / (1 + zeta*dt)) ** np.arange(len(time))

    # update data in plots
    line_exact1.set_data(time, velocity_exact)
    line_explicit.set_data(time, velocity_explicit)
    line_explicit.set_label(f"Explicit dt={dt:.2f}")

    line_exact2.set_data(time, velocity_exact)
    line_implicit.set_data(time, velocity_implicit)
    line_implicit.set_label(f"Implicit dt={dt:.2f}")

    # rescale axes
    ax1.relim(); ax1.autoscale()
    ax2.relim(); ax2.autoscale()
    ax1.legend(); ax2.legend()
    fig.canvas.draw_idle()

# connect slider
dt_slider.on_changed(update)

plt.show()
