import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout)
from MethodsForSolving import ThreeBodySolver


class OrbitPlotWindow(QMainWindow):
    """Окно для визуализации орбиты"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Визуализация орбиты - Ограниченная задача трех тел")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Создание matplotlib figure
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def plot_orbit(self, sol, mu, init_states, method, center_point=(0, 0), bounds=(1.5, 1.0)):
        """Построение графика орбиты

        Args:
            sol: решение системы ОДУ
            mu: массовый параметр
            init_states: начальные условия
            method: метод интегрирования
            center_point: центральная точка графика (x_center, y_center)
            bounds: размеры границ по ox и oy (x_bound, y_bound)
        """
        self.figure.clear()

        # Создание основного графика
        ax = self.figure.add_subplot(111)

        x, y, u, v = sol.y
        t = sol.t

        # Основной график орбиты
        ax.plot(x, y, 'b-', linewidth=1, label='Траектория')
        ax.plot(x[0], y[0], 'go', markersize=8, label='Начало')
        ax.plot(x[-1], y[-1], 'ro', markersize=8, label='Конец')

        # Точки Лагранжа и массивные тела
        self.plot_lagrange_points(ax, mu)

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(f'Орбита в ограниченной задаче трех тел\nμ={mu}, метод: {method}')
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.axis('equal')

        # Установка границ графика на основе новых параметров
        x_center, y_center = center_point
        x_bound, y_bound = bounds

        ax.set_xlim(x_center - x_bound, x_center + x_bound)
        ax.set_ylim(y_center - y_bound, y_center + y_bound)

        self.figure.tight_layout()
        self.canvas.draw()

    def plot_lagrange_points(self, ax, mu):
        """Отображение точек Лагранжа и массивных тел"""
        # Массивные тела (более крупные и заметные)
        ax.plot(-mu, 0, 'ko', markersize=10, label='M1')
        ax.plot(-mu + 1, 0, 'ko', markersize=10, label='M2')
        ax.text(-mu, 0.1, 'M1', ha='center', fontsize=10)
        ax.text(-mu + 1, 0.1, 'M2', ha='center', fontsize=10)

        # Точки Лагранжа L1, L2, L3 (коллинеарные)
        # Приближенные вычисления для точек Лагранжа
        alpha = (mu / 3) ** (1/3)

        L1_x, L2_x, L3_x = ThreeBodySolver.get_lagrange_points_simple(mu)

        # L4 и L5 (треугольные)
        L4_x = 0.5 - mu
        L4_y = np.sqrt(3) / 2
        L5_x = 0.5 - mu
        L5_y = -np.sqrt(3) / 2

        # Отображение всех точек Лагранжа
        lagrange_points = [
            (L1_x, 0, 'L1'),
            (L2_x, 0, 'L2'),
            (L3_x, 0, 'L3'),
            (L4_x, L4_y, 'L4'),
            (L5_x, L5_y, 'L5')
        ]

        for i, (lx, ly, label) in enumerate(lagrange_points):
            color = 'red' if i < 3 else 'green'  # Коллинеарные красные, треугольные зеленые
            ax.plot(lx, ly, '^', color=color, markersize=8, markeredgecolor='black')
            ax.text(lx, ly + 0.04, label, ha='center', fontsize=10,
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.7))