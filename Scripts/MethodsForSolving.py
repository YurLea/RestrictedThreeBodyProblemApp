from scipy.integrate import solve_ivp
import numpy as np

class ThreeBodySolver:
    """Решатель ограниченной задачи трех тел"""

    @staticmethod
    def equations(t, state, mu):
        """Уравнения движения ограниченной задачи трех тел"""
        x, y, u, v = state

        # Расстояния до двух массивных тел
        r1 = np.sqrt((x + mu) ** 2 + y ** 2)
        r2 = np.sqrt((x - 1 + mu) ** 2 + y ** 2)

        # Уравнения движения
        dxdt = u
        dydt = v
        dudt = (2 * v + x -
                (1 - mu) * (x + mu) / r1 ** 3 - mu * (x + mu - 1) / r2 ** 3)
        dvdt = (-2 * u + y -
                (1 - mu) * y / r1 ** 3 - mu * y / r2 ** 3)

        return [dxdt, dydt, dudt, dvdt]

    @staticmethod
    def get_lagrange_points_simple(mu):
        """Упрощенное получение точек лагранжа с поиском в известных интервалах"""
        tol = 1e-6
        l1, l2, l3 = 0, 0, 0

        # Известные приближенные положения точек Лагранжа
        # L3 слева от m1, L1 между m1 и m2, L2 справа от m2
        search_intervals = [
            (-1.5, -0.5),  # Для L3 (слева от центра масс)
            (0.5, 0.9),  # Для L1 (между телами)
            (1.1, 1.5)  # Для L2 (справа от m2)
        ]

        def equation(x):
            r1 = np.sqrt((x + mu) ** 2)
            r2 = np.sqrt((x - 1 + mu) ** 2)
            return x - (1 - mu) * (x + mu) / r1 ** 3 - mu * (x + mu - 1) / r2 ** 3

        for i, (a, b) in enumerate(search_intervals):
            # Поиск корня методом деления пополам
            left, right = a, b
            f_left = equation(left)

            for _ in range(50):  # Максимум 50 итераций
                mid = (left + right) / 2
                f_mid = equation(mid)

                if abs(f_mid) < tol:
                    if i == 0:
                        l3 = mid
                    elif i == 1:
                        l1 = mid
                    elif i == 2:
                        l2 = mid
                    break

                if f_left * f_mid < 0:
                    right = mid
                else:
                    left = mid
                    f_left = f_mid

        return l1, l2, l3

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