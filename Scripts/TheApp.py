import numpy as np
from MethodsForSolving import solve_system
import matplotlib.pyplot as plt

# Solultion
init_states = [0.65, 0.0, 0, 2.07]
method = 'RK45'
t_span = (0, 30)
t_eval = np.linspace(0, 30, 200000)

sol = solve_system(init_states, method, t_span, t_eval, 0.5)

# Visualization
plt.plot(sol.y[0], sol.y[1])
plt.title('Orbit')
plt.xlabel('x')
plt.ylabel('y')

plt.tight_layout()
plt.show()