import numpy as np
import matplotlib.pyplot as plt

c = 0.5
m = 1
dt_values = np.arange(0.1, 1, 0.2)   # time steps
print("dt values:", dt_values)

zeta = c / m
v0 = 1

plt.figure(figsize=(12, 5))

# prepare subplots
ax1 = plt.subplot(1, 2, 1)   # Explicit
ax2 = plt.subplot(1, 2, 2)   # Implicit

for dt in dt_values:  # ---- outer loop over dt ----
    time = np.arange(0, 5 + dt, dt)

    velocity_explicit = np.zeros(len(time))
    velocity_implicit = np.zeros(len(time))
    velocity_exact    = np.zeros(len(time))

    velocity_explicit[0] = v0
    velocity_implicit[0] = v0
    velocity_exact[0]    = v0

    # ---- inner loop for time-stepping ----
    for ii in range(len(time) - 1):
        velocity_explicit[ii+1] = velocity_explicit[ii] * (1 - zeta*dt)
        velocity_implicit[ii+1] = velocity_implicit[ii] * (1 / (1 + zeta*dt))
        velocity_exact[ii+1]    = v0 * np.exp(-zeta * time[ii+1])

    # plot on subplots
    ax1.plot(time, velocity_explicit, marker='o', label=f"Explicit dt={dt:.1f}")
    ax2.plot(time, velocity_implicit, marker='s', label=f"Implicit dt={dt:.1f}")

# add exact solution only once (using finest dt for smooth curve)
ax1.plot(time, velocity_exact, linestyle="--", color="black", linewidth=2, label="Exact")
ax2.plot(time, velocity_exact, linestyle="--", color="black", linewidth=2, label="Exact")

# formatting
ax1.set_xlabel("Time (s)", fontsize=14)
ax1.set_ylabel("Velocity (m/s)", fontsize=14)
ax1.set_title("Explicit Euler vs Exact", fontsize=16)
ax1.legend(fontsize=10)
ax1.grid(True)

ax2.set_xlabel("Time (s)", fontsize=14)
ax2.set_ylabel("Velocity (m/s)", fontsize=14)
ax2.set_title("Implicit Euler vs Exact", fontsize=16)
ax2.legend(fontsize=10)
ax2.grid(True)

plt.tight_layout()
plt.show()
