from scipy.integrate import solve_ivp
import numpy as np


def system_of_problem(t, states, mu): # mass parameter
    """
    Restricted 3 body problem
    """
    x, y, u, v = states

    r1 = np.sqrt((x - mu) ** 2 + y ** 2)
    r2 = np.sqrt((x - mu + 1) ** 2 + y ** 2)

    dxdt = u
    dydt = v
    dudt = (2 * v + (1 - mu) * (x - mu) + mu * (x + 1 - mu) -
            (1 - mu) * (x - mu) / r1 ** 3 - mu * (x - mu + 1) / r2 ** 3)
    dvdt = (-2 * u + (1 - mu) * y + mu * y -
            (1 - mu) * y / r1 ** 3 - mu * y / r2 ** 3)

    return [dxdt, dydt, dudt, dvdt]

def solve_system(states, method, t_span, t_eval, mu):
    return solve_ivp(system_of_problem, t_span, states, t_eval=t_eval,
                method=method, rtol=1e-12, atol=1e-12, args=(mu,))