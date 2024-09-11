import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QGridLayout
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QPalette


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mega Cool Calculator with Animations")
        self.setFixedSize(400, 500)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

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
            button.clicked.connect(self.button_clicked)

            # Добавление анимации
            self.animate_button(button)
            self.button_grid.addWidget(button, row, col)

    # Анимация кнопок при наведении курсора
    def animate_button(self, button):
        button.setStyleSheet(button.styleSheet() + """
            QPushButton:hover {
                background-color: #1ABC9C;
                transition: background-color 0.3s ease;
            }
        """)

    # Обработка нажатий на кнопки
    def button_clicked(self):
        button = self.sender()
        text = button.text()

        if text == 'C':
            self.display.setText('')
        elif text == '=':
            try:
                expression = self.display.text()
                if not expression:  # Если поле ввода пустое
                    raise ValueError("Поле ввода пустое")
                result = str(eval(expression))  # Оцениваем выражение
                self.display.setText(result)
            except ZeroDivisionError:
                self.display.setText("Деление на 0!")
            except Exception as e:
                self.display.setText("Ошибка")
        else:
            self.display.setText(self.display.text() + text)

    # Анимация изменения цвета окна при нажатии клавиши
    def animate_background(self):
        self.anim = QPropertyAnimation(self.central_widget, b"windowOpacity")
        self.anim.setDuration(500)
        self.anim.setStartValue(0.8)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QEasingCurve.OutBounce)
        self.anim.start()


def main():
    app = QApplication(sys.argv)

    # Настройка основной цветовой палитры для приложения
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#34495E"))
    app.setPalette(palette)

    window = Calculator()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
