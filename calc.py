import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QGridLayout, QMessageBox, QDialog, QVBoxLayout as VLayout, QHBoxLayout as HLayout, QLabel, QColorDialog, QCheckBox, QSpinBox
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal
from PyQt5.QtGui import QColor, QPalette

class SettingsDialog(QDialog):
    settings_changed = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки")
        self.layout = VLayout()

        # Настройка цветов
        self.color_layout = HLayout()
        self.color_label = QLabel("Цвет фона:")
        self.color_button = QPushButton("Выбрать цвет")
        self.color_button.clicked.connect(self.choose_background_color)
        self.color_layout.addWidget(self.color_label)
        self.color_layout.addWidget(self.color_button)
        self.layout.addLayout(self.color_layout)

        # Настройка цвета кнопок
        self.button_color_layout = HLayout()
        self.button_color_label = QLabel("Цвет кнопок:")
        self.button_color_button = QPushButton("Выбрать цвет")
        self.button_color_button.clicked.connect(self.choose_button_color)
        self.button_color_layout.addWidget(self.button_color_label)
        self.button_color_layout.addWidget(self.button_color_button)
        self.layout.addLayout(self.button_color_layout)

        # Включение/выключение анимаций
        self.animation_layout = HLayout()
        self.animation_checkbox = QCheckBox("Включить анимации")
        self.animation_checkbox.setChecked(True)
        self.animation_layout.addWidget(self.animation_checkbox)
        self.layout.addLayout(self.animation_layout)

        # Продолжительность анимации
        self.duration_layout = HLayout()
        self.duration_label = QLabel("Продолжительность анимации (мс):")
        self.duration_spinbox = QSpinBox()
        self.duration_spinbox.setRange(100, 2000)
        self.duration_spinbox.setValue(300)
        self.duration_layout.addWidget(self.duration_label)
        self.duration_layout.addWidget(self.duration_spinbox)
        self.layout.addLayout(self.duration_layout)

        # Кнопка сохранения настроек
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

    def choose_background_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.background_color = color

    def choose_button_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.button_color = color

    def save_settings(self):
        settings = {
            'background_color': getattr(self, 'background_color', None),
            'button_color': getattr(self, 'button_color', None),
            'enable_animations': self.animation_checkbox.isChecked(),
            'animation_duration': self.duration_spinbox.value()
        }
        self.settings_changed.emit(settings)
        self.close()


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mega Cool Calculator with Animations")
        self.setFixedSize(400, 500)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        # Настройки по умолчанию
        self.default_settings = {
            'background_color': QColor("#34495E"),
            'button_color': QColor("#3498DB"),
            'enable_animations': True,
            'animation_duration': 300
        }

        # Основной лейаут
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        # Поле для ввода
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFixedHeight(70)
        self.display.setStyleSheet("font-size: 30px; background-color: #2C3E50; color: white; border: none;")
        self.layout.addWidget(self.display)
        
        # Сетка для кнопок
        self.button_grid = QGridLayout()
        self.layout.addLayout(self.button_grid)
        
        # Определяем кнопки
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('C', 3, 0), ('0', 3, 1), ('=', 3, 2), ('+', 3, 3),
        ]
        
        # Добавляем кнопки в сетку
        for btn_text, row, col in buttons:
            button = QPushButton(btn_text)
            button.setFixedSize(80, 80)
            button.setStyleSheet("""
                QPushButton {
                    font-size: 24px;
                    background-color: #3498DB;
                    color: white;
                    border-radius: 10px;
                }
                QPushButton:pressed {
                    background-color: #2980B9;
                }
            """)
            button.clicked.connect(lambda checked, b=button: self.on_button_clicked(b))
            self.animate_button(button)
            self.button_grid.addWidget(button, row, col)

        # Создание диалогового окна настроек
        self.settings_dialog = SettingsDialog(self)
        self.settings_dialog.settings_changed.connect(self.apply_settings)

        # Кнопка настроек
        self.settings_button = QPushButton("Настройки")
        self.settings_button.clicked.connect(self.show_settings)
        self.layout.addWidget(self.settings_button)

        # Применение начальных настроек
        self.apply_initial_settings()

    def apply_initial_settings(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, self.default_settings['background_color'])
        self.setPalette(palette)
        for btn in self.findChildren(QPushButton):
            btn.setStyleSheet(f"""
                QPushButton {{
                    font-size: 24px;
                    background-color: {self.default_settings['button_color'].name()};
                    color: white;
                    border-radius: 10px;
                }}
                QPushButton:pressed {{
                    background-color: {self.default_settings['button_color'].darker(120).name()};
                }}
            """)

    def animate_button(self, button):
        if self.default_settings['enable_animations']:
            button.setStyleSheet(button.styleSheet() + f"""
                QPushButton:hover {{
                    background-color: #1ABC9C;
                    transition: background-color {self.default_settings['animation_duration']}ms ease;
                }}
            """)

    def on_button_clicked(self, button):
        text = button.text()
        if text == 'C':
            self.clear_display()
        elif text == '=':
            self.calculate_result()
        else:
            self.update_display(text)

    def clear_display(self):
        self.display.setText('')

    def calculate_result(self):
        expression = self.display.text()
        try:
            if not expression:
                raise ValueError("Поле ввода пустое")
            result = str(eval(expression))
            self.display.setText(result)
        except ZeroDivisionError:
            self.show_error_message("Деление на 0!")
        except Exception as e:
            self.show_error_message("Ошибка")

    def update_display(self, text):
        current_text = self.display.text()
        self.display.setText(current_text + text)

    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText(message)
        msg_box.setWindowTitle("Ошибка")
        msg_box.exec_()

    def show_settings(self):
        self.settings_dialog.show()

    def apply_settings(self, settings):
        if settings['background_color']:
            palette = QPalette()
            palette.setColor(QPalette.Window, settings['background_color'])
            self.setPalette(palette)
        if settings['button_color']:
            for btn in self.findChildren(QPushButton):
                btn.setStyleSheet(f"""
                    QPushButton {{
                        font-size: 24px;
                        background-color: {settings['button_color'].name()};
                        color: white;
                        border-radius: 10px;
                    }}
                    QPushButton:pressed {{
                        background-color: {settings['button_color'].darker(120).name()};
                    }}
                """)
        self.default_settings.update(settings)
        for btn in self.findChildren(QPushButton):
            self.animate_button(btn)


def main():
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
