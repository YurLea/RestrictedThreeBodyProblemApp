import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


def nonlinear_system(t, states):
    """
    Restricted 3 body problem
    """
    x, y, u, v = states

    mu = 0.5

    r1 = np.sqrt((x - mu)**2 + y**2)
    r2 = np.sqrt((x - mu + 1)**2 + y**2)

    dxdt = u
    dydt = v
    dudt = (2*v + (1 - mu) * (x - mu) + mu * (x + 1 - mu) -
            (1-mu) * (x - mu) / r1**3 - mu * (x - mu + 1) / r2**3)
    dvdt = (-2*u + (1 - mu) * y + mu * y -
            (1-mu) * y / r1**3 - mu * y / r2**3)

    return [dxdt, dydt, dudt, dvdt]

# Solultion
init_states = [0.6, 0.0, 0, 1.0]
t_span = (0, 5)
t_eval = np.linspace(0, 5, 100000)

sol = solve_ivp(nonlinear_system, t_span, init_states, t_eval=t_eval,
                method='RK45', rtol=1e-12, atol=1e-12)

# Visualization
plt.plot(sol.y[0], sol.y[1])
plt.title('Orbit')
plt.xlabel('x')
plt.ylabel('y')

plt.tight_layout()
plt.show()