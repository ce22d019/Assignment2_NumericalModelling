import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Parameters
c = 0.5
m = 1
zeta = c / m
v0 = 1
t_end = 5

# Stability boundary for Explicit Euler
dt_crit = 2.0    # For our case, dt_crit = 2

# Initial dt
dt0 = 0.1

# Time array for plotting (ensure endpoint is included)
time = np.arange(0, t_end + dt0, dt0)

# Exact solution
velocity_exact = v0 * np.exp(-zeta * time)

# Explicit Euler (initial)
velocity_explicit = v0 * (1 - zeta*dt0) ** np.arange(len(time))

# Implicit Euler (initial)
velocity_implicit = v0 * (1 / (1 + zeta*dt0)) ** np.arange(len(time))

# --- Plot setup ---
fig, ax = plt.subplots(figsize=(9,6))
plt.subplots_adjust(bottom=0.25)

line_exact, = ax.plot(time, velocity_exact, 'k-', lw=2, label="Exact")
line_explicit, = ax.plot(time, velocity_explicit, 'r--', lw=2,
                         label=f"Explicit Euler (dt={dt0:.2f})")
line_implicit, = ax.plot(time, velocity_implicit, 'b-.', lw=2,
                         label=f"Implicit Euler (dt={dt0:.2f})")

# Add stability boundary visualization (only for explicit)
ax.axhline(y=0, color='gray', linestyle='--', linewidth=1)  # baseline
ax.axvspan(0, dt_crit, facecolor='green', alpha=0.08, label="Stable region (Explicit)")
ax.axvspan(dt_crit, t_end, facecolor='red', alpha=0.08, label="Unstable region (Explicit)")
ax.axvline(x=dt_crit, color='cyan', linestyle='--', linewidth=2, label="Stability limit (dt=2)")

# --- Moving vertical line for current dt (follows slider) ---
dt_marker = ax.axvline(x=dt0, color='magenta', linestyle='-', linewidth=2, label="Current dt")

# Labels & legend
ax.set_xlabel("Time", fontsize=14)
ax.set_ylabel("Velocity", fontsize=14)
ax.set_title("Stability Check: Explicit vs Implicit Euler", fontsize=16)
ax.legend(fontsize=10, loc="upper right")
ax.grid(True, ls="--")

# Slider axis
ax_slider = plt.axes([0.2, 0.1, 0.6, 0.03])
slider_dt = Slider(ax_slider, "dt", 0.01, 5.0, valinit=dt0, valstep=0.01)

# Update function for slider
def update(val):
    dt = slider_dt.val
    # include endpoint
    time = np.arange(0, t_end + dt, dt)

    velocity_exact = v0 * np.exp(-zeta * time)
    velocity_explicit = v0 * (1 - zeta*dt) ** np.arange(len(time))
    velocity_implicit = v0 * (1 / (1 + zeta*dt)) ** np.arange(len(time))

    line_exact.set_data(time, velocity_exact)
    line_explicit.set_data(time, velocity_explicit)
    line_implicit.set_data(time, velocity_implicit)

    line_explicit.set_label(f"Explicit Euler (dt={dt:.2f})")
    line_implicit.set_label(f"Implicit Euler (dt={dt:.2f})")

    # move the current-dt vertical marker
    dt_marker.set_xdata([dt, dt])

    ax.set_xlim(0, t_end)   # lock x-axis to 5s always
    ax.relim()
    ax.autoscale_view(scaley=True)  # rescale only y
    ax.legend(fontsize=10, loc="upper right")
    fig.canvas.draw_idle()

slider_dt.on_changed(update)

plt.show()
