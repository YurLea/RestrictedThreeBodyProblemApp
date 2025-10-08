from scipy.integrate import solve_ivp
import numpy as np

class ThreeBodySolver:
    """Решатель ограниченной задачи трех тел"""

    @staticmethod
    def equations(t, state, mu):
        """Уравнения движения ограниченной задачи трех тел"""
        x, y, u, v = state

        # Расстояния до двух массивных тел
        r1 = np.sqrt((x - mu) ** 2 + y ** 2)
        r2 = np.sqrt((x + 1 - mu) ** 2 + y ** 2)

        # Уравнения движения
        dxdt = u
        dydt = v
        dudt = (2 * v + (1 - mu) * (x - mu) + mu * (x + 1 - mu) -
                (1 - mu) * (x - mu) / r1 ** 3 - mu * (x - mu + 1) / r2 ** 3)
        dvdt = (-2 * u + (1 - mu) * y + mu * y -
                (1 - mu) * y / r1 ** 3 - mu * y / r2 ** 3)

        return [dxdt, dydt, dudt, dvdt]

    def solve_system(self, init_states, method, t_span, t_eval, mu):
        """Решение системы уравнений"""
        sol = solve_ivp(
            fun=self.equations,
            t_span=t_span,
            y0=init_states,
            method=method,
            t_eval=t_eval,
            args=(mu,),
            rtol=1e-8,
            atol=1e-11
        )
        return sol