import sys
import numpy as np
import PyQt5 as Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QGroupBox, QLabel, QLineEdit,
                             QComboBox, QPushButton, QGridLayout, QDoubleSpinBox,
                             QTextEdit, QFormLayout, QMessageBox)
from MethodsForSolving import ThreeBodySolver
from PlotWindow import OrbitPlotWindow


class MainWindow(QMainWindow):
    """Главное окно приложения"""

    def __init__(self):
        super().__init__()
        self.solver = ThreeBodySolver()
        self.plot_window = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Исследование ограниченной задачи трех тел")
        self.setGeometry(100, 100, 900, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Левая панель - управление
        left_panel = self.create_control_panel()
        main_layout.addWidget(left_panel)

        # Правая панель - информация и уравнения
        right_panel = self.create_info_panel()
        main_layout.addWidget(right_panel)

    def create_control_panel(self):
        """Создание панели управления"""
        panel = QGroupBox("Параметры задачи")
        layout = QVBoxLayout()

        # Начальные условия
        conditions_group = QGroupBox("Начальные условия")
        conditions_layout = QGridLayout()

        conditions_layout.addWidget(QLabel("x₀:"), 0, 0)
        self.x0_input = QDoubleSpinBox()
        self.x0_input.setRange(-10, 10)
        self.x0_input.setValue(0.65)
        self.x0_input.setDecimals(3)
        conditions_layout.addWidget(self.x0_input, 0, 1)

        conditions_layout.addWidget(QLabel("y₀:"), 1, 0)
        self.y0_input = QDoubleSpinBox()
        self.y0_input.setRange(-10, 10)
        self.y0_input.setValue(0.0)
        self.y0_input.setDecimals(3)
        conditions_layout.addWidget(self.y0_input, 1, 1)

        conditions_layout.addWidget(QLabel("u₀ (vx):"), 2, 0)
        self.u0_input = QDoubleSpinBox()
        self.u0_input.setRange(-10, 10)
        self.u0_input.setValue(0.0)
        self.u0_input.setDecimals(3)
        conditions_layout.addWidget(self.u0_input, 2, 1)

        conditions_layout.addWidget(QLabel("v₀ (vy):"), 3, 0)
        self.v0_input = QDoubleSpinBox()
        self.v0_input.setRange(-10, 10)
        self.v0_input.setValue(2.07)
        self.v0_input.setDecimals(3)
        conditions_layout.addWidget(self.v0_input, 3, 1)

        conditions_group.setLayout(conditions_layout)
        layout.addWidget(conditions_group)

        # Параметры решения
        params_group = QGroupBox("Параметры решения")
        params_layout = QGridLayout()

        params_layout.addWidget(QLabel("Массовый параметр (μ):"), 0, 0)
        self.mu_input = QDoubleSpinBox()
        self.mu_input.setRange(0.001, 0.5)
        self.mu_input.setValue(0.5)
        self.mu_input.setSingleStep(0.01)
        self.mu_input.setDecimals(4)
        params_layout.addWidget(self.mu_input, 0, 1)

        params_layout.addWidget(QLabel("Метод решения:"), 1, 0)
        self.method_combo = QComboBox()
        self.method_combo.addItems(['RK45', 'DOP853', 'LSODA'])
        params_layout.addWidget(self.method_combo, 1, 1)

        params_layout.addWidget(QLabel("Время моделирования:"), 2, 0)
        self.time_input = QDoubleSpinBox()
        self.time_input.setRange(0.1, 1000)
        self.time_input.setValue(30)
        self.time_input.setSingleStep(5)
        params_layout.addWidget(self.time_input, 2, 1)

        params_layout.addWidget(QLabel("Количество точек:"), 3, 0)
        self.points_input = QDoubleSpinBox()
        self.points_input.setRange(100, 1000000)
        self.points_input.setValue(20000)  # Уменьшено для быстродействия
        self.points_input.setSingleStep(1000)
        params_layout.addWidget(self.points_input, 3, 1)

        params_group.setLayout(params_layout)
        layout.addWidget(params_group)

        # Настройки графика
        self.settings_group = QGroupBox("Параметры области отображения графика")
        group_layout = QFormLayout()

        # Поля для ввода координат центра
        self.center_x_input = QLineEdit()
        self.center_x_input.setPlaceholderText("0.0")

        self.center_y_input = QLineEdit()
        self.center_y_input.setPlaceholderText("0.0")

        # Поля для ввода размеров области
        self.bounds_x_input = QLineEdit()
        self.bounds_x_input.setPlaceholderText("5.0")
        self.bounds_y_input = QLineEdit()
        self.bounds_y_input.setPlaceholderText("5.0")

        # Добавляем поля в форму
        group_layout.addRow("Центр X:", self.center_x_input)
        group_layout.addRow("Центр Y:", self.center_y_input)
        group_layout.addRow("Размер по OX:", self.bounds_x_input)
        group_layout.addRow("Размер по OY:", self.bounds_y_input)

        self.settings_group.setLayout(group_layout)
        layout.addWidget(self.settings_group)

        # Кнопка применения настроек
        self.apply_button = QPushButton("Применить настройки")
        self.apply_button.clicked.connect(self.apply_settings)
        layout.addWidget(self.apply_button)

        # Кнопки управления
        self.solve_button = QPushButton("Решить задачу и построить график")
        self.solve_button.clicked.connect(self.solve_problem)
        layout.addWidget(self.solve_button)

        panel.setLayout(layout)
        return panel

    def create_info_panel(self):
        """Создание панели с информацией и уравнениями"""
        panel = QGroupBox("Уравнения и информация")
        layout = QVBoxLayout()

        # Отображение уравнений
        equations_text = QTextEdit()
        equations_text.setReadOnly(True)
        equations_text.setHtml("""
        <h3>Ограниченная задача трех тел</h3>
        <p><b>Система уравнений в безразмерной форме:</b></p>
        <pre>
    dx/dt = u
    dy/dt = v
    du/dt = 2v + x - (1-μ)(x+μ)/r₁³ - μ(x-1+μ)/r₂³
    dv/dt = -2u + y - (1-μ)y/r₁³ - μy/r₂³
        </pre>
        <p>где:</p>
        <ul>
        <li>r₁ = √((x-μ)² + y²) - расстояние до тела M1</li>
        <li>r₂ = √((x+1-μ)² + y²) - расстояние до тела M2</li>
        <li>μ - массовый параметр (0 < μ ≤ 0.5)</li>
        </ul>
        <p><b>На графике отображаются:</b></p>
        <ul>
        <li>Синяя линия - траектория третьего тела</li>
        <li>Зеленая точка - начало траектории</li>
        <li>Красная точка - конец траектории</li>
        <li>Черные круги - массивные тела M1 и M2</li>
        <li>Красные треугольники - коллинеарные точки Лагранжа L1, L2, L3</li>
        <li>Зеленые треугольники - треугольные точки Лагранжа L4, L5</li>
        </ul>
        <p><b>Текущие начальные условия:</b></p>
        <p id="current_conditions">x₀=0.65, y₀=0.0, u₀=0.0, v₀=2.07</p>
        """)
        layout.addWidget(equations_text)
        self.equations_text = equations_text

        # Предустановки
        presets_group = QGroupBox("Быстрые настройки")
        presets_layout = QVBoxLayout()

        earth_moon_btn = QPushButton("Система Земля-Луна (μ=0.01215)")
        earth_moon_btn.clicked.connect(lambda: self.set_preset(0.01215, 0.65, 0.0, 0.0, 2.07))
        presets_layout.addWidget(earth_moon_btn)

        sun_jupiter_btn = QPushButton("Система Солнце-Юпитер (μ=0.0009537)")
        sun_jupiter_btn.clicked.connect(lambda: self.set_preset(0.0009537, 0.65, 0.0, 0.0, 2.07))
        presets_layout.addWidget(sun_jupiter_btn)

        equal_mass_btn = QPushButton("Равные массы (μ=0.5)")
        equal_mass_btn.clicked.connect(lambda: self.set_preset(0.5, 0.65, 0.0, 0.0, 2.07))
        presets_layout.addWidget(equal_mass_btn)

        presets_group.setLayout(presets_layout)
        layout.addWidget(presets_group)

        panel.setLayout(layout)
        return panel

    def set_preset(self, mu, x0, y0, u0, v0):
        """Установка предустановленных параметров"""
        self.mu_input.setValue(mu)
        self.x0_input.setValue(x0)
        self.y0_input.setValue(y0)
        self.u0_input.setValue(u0)
        self.v0_input.setValue(v0)

        # Обновление отображаемых условий
        self.update_equations_display()

    def update_equations_display(self):
        """Обновление отображаемых начальных условий"""
        conditions_text = f"x₀={self.x0_input.value():.3f}, y₀={self.y0_input.value():.3f}, u₀={self.u0_input.value():.3f}, v₀={self.v0_input.value():.3f}"
        html = self.equations_text.toHtml()
        # Обновляем только часть с условиями
        new_html = html.split('<p id="current_conditions">')[
                       0] + f'<p id="current_conditions">{conditions_text}</p></body></html>'
        self.equations_text.setHtml(new_html)

    def apply_settings(self):
        """Обработчик нажатия кнопки применения настроек"""
        try:
            # Получаем значения из полей ввода
            center_x = float(self.center_x_input.text() or 0.0)
            center_y = float(self.center_y_input.text() or 0.0)
            bounds_x = float(self.bounds_x_input.text() or 5.0)
            bounds_y = float(self.bounds_y_input.text() or 5.0)

            # Проверяем валидность размеров
            if bounds_x <= 0 or bounds_y <= 0:
                QMessageBox.warning(self, "Ошибка", "Размеры области должны быть положительными числами")
                return

            # Здесь передаем параметры в метод построения графика
            self.update_plot_parameters(center_x, center_y, bounds_x, bounds_y)

            QMessageBox.information(self, "Успех", "Параметры графика обновлены!")

        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите корректные числовые значения")

    def update_plot_parameters(self, center_x, center_y, bounds_x, bounds_y):
        """
        Обновляет параметры графика
        Эту функцию нужно интегрировать с вашим существующим кодом
        """
        print(f"Новые параметры графика: Центр({center_x}, {center_y}), Размер({bounds_x}, {bounds_y})")
        # Здесь вызывайте ваш метод plot_orbit с новыми параметрами:
        #self.plot_orbit(sol, mu, init_states, method,
        #                center_point=(center_x, center_y),
        #                bounds=(bounds_x, bounds_y))

    def solve_problem(self):
        """Решение задачи и построение графика"""
        try:
            # Получение параметров
            init_states = [
                self.x0_input.value(),
                self.y0_input.value(),
                self.u0_input.value(),
                self.v0_input.value()
            ]
            method = self.method_combo.currentText()
            t_max = self.time_input.value()
            n_points = int(self.points_input.value())
            mu = self.mu_input.value()

            t_span = (0, t_max)
            t_eval = np.linspace(0, t_max, n_points)

            # Решение системы
            sol = self.solver.solve_system(init_states, method, t_span, t_eval, mu)

            # Получение параметров графика с обработкой ошибок
            try:
                center_x = float(self.center_x_input.text())
                center_y = float(self.center_y_input.text())
                bounds_x = float(self.bounds_x_input.text())
                bounds_y = float(self.bounds_y_input.text())
            except ValueError:
                QMessageBox.warning(
                    self,
                    "Ошибка ввода параметров графика",
                    "Пожалуйста, введите корректные числовые значения для всех параметров графика:\n"
                    "- Координата X центра\n"
                    "- Координата Y центра\n"
                    "- Размер области по OX\n"
                    "- Размер области по OY\n\n"
                    "Пример: 0.0, 1.5, 3.0, 2.5"
                )
                return

            # Проверка на положительные размеры области
            if bounds_x <= 0 or bounds_y <= 0:
                QMessageBox.warning(
                    self,
                    "Некорректные размеры области",
                    "Размеры области отображения должны быть положительными числами.\n"
                    f"Получено: OX={bounds_x}, OY={bounds_y}"
                )
                return

            # Создание или обновление окна с графиком
            if self.plot_window is None:
                self.plot_window = OrbitPlotWindow()

            self.plot_window.plot_orbit(
                sol, mu, init_states, method,
                (center_x, center_y),
                (bounds_x, bounds_y)
            )
            self.plot_window.show()

            # Обновление отображаемых условий
            self.update_equations_display()

        except Exception as e:
            error_msg = f"Ошибка при решении системы: {str(e)}"
            print(error_msg)
            QMessageBox.critical(self, "Ошибка вычислений", error_msg)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()