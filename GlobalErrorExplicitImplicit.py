import numpy as np
import matplotlib.pyplot as plt

# Parameters
c = 0.5
m = 1
zeta = c / m
v0 = 1

# Time step sizes to test (logarithmically spaced)
dts = [0.1 * 0.1**(n-1) for n in range(1, 9)]

# Storage for errors
errors_explicit = []
errors_implicit = []

# Loop over dt values
for dt in dts:
    time = np.arange(0, 5 + dt, dt)   # time array
    
    # Exact solution
    velocity_exact = v0 * np.exp(-zeta * time)
    
    # Explicit Euler
    velocity_explicit = v0 * (1 - zeta*dt) ** np.arange(len(time))
    
    # Implicit Euler
    velocity_implicit = v0 * (1 / (1 + zeta*dt)) ** np.arange(len(time))
    
    # RMS errors (clip to avoid nan when unstable)
    err_exp = np.sqrt(np.mean((velocity_explicit - velocity_exact)**2))
    err_imp = np.sqrt(np.mean((velocity_implicit - velocity_exact)**2))
    
    errors_explicit.append(err_exp)
    errors_implicit.append(err_imp) 

# --- Log-Log Plot ---
plt.figure(figsize=(8,6))
plt.loglog(dts, errors_explicit, 'o-', label="Explicit Euler")
plt.loglog(dts, errors_implicit, 's-', label="Implicit Euler")

plt.xlabel("Time step size (dt)", fontsize=14)
plt.ylabel("Global RMS Error", fontsize=14)
plt.title("Error vs Time Step (Log-Log)", fontsize=16)
plt.legend(fontsize=12)
plt.grid(True, which="both", ls="--")
plt.show()
