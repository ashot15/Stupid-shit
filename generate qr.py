import random
import qrcode
from PIL import Image
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

class QRCodeGenerator(QWidget):
    def __init__(self):
        super().__init__()

        # Установка окна
        self.setWindowTitle("QR-CODE MAKER")
        self.setGeometry(100, 100, 350, 500)

        # Создание макета
        layout = QVBoxLayout()

        # Установка палитры для мягких цветов
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#f0f0f5"))
        palette.setColor(QPalette.WindowText, Qt.black)
        self.setPalette(palette)

        # Стили кнопок
        self.button_style = """
            QPushButton {
                background-color: #87CEEB;
                color: #ffffff;
                font-size: 14px;
                font-weight: bold;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #00BFFF;
            }
        """

        # Поле ввода текста для QR-кода
        self.label_text = QLabel("Введи текст для генерации:")
        layout.addWidget(self.label_text)
        self.text_input = QLineEdit(self)
        layout.addWidget(self.text_input)

        # Выбор размера QR-кода
        self.label_size = QLabel("Размер QR-кода:")
        layout.addWidget(self.label_size)
        self.size_input = QLineEdit(self)
        self.size_input.setText("10")
        layout.addWidget(self.size_input)

        # Выбор сложности QR-кода
        self.label_level = QLabel("Сложность QR-кода:")
        layout.addWidget(self.label_level)
        self.level_input = QSpinBox(self)
        self.level_input.setMinimum(1)
        self.level_input.setMaximum(40)
        layout.addWidget(self.level_input)

        # Выбор цвета QR-кода
        self.label_color = QLabel("Цвет QR-кода:")
        layout.addWidget(self.label_color)
        self.color_input = QComboBox(self)
        self.color_input.addItems(["Black", "Red", "Blue", "Green", "Purple", "Teal"])
        layout.addWidget(self.color_input)

        # Выбор цвета фона QR-кода
        self.label_bg_color = QLabel("Цвет фона:")
        layout.addWidget(self.label_bg_color)
        self.bg_color_input = QComboBox(self)
        self.bg_color_input.addItems(["White", "Light Yellow", "Light Pink", "Light Blue", "Mint"])
        layout.addWidget(self.bg_color_input)

        # Поле для ввода имени файла
        self.label_filename = QLabel("Название файла (без расширения):")
        layout.addWidget(self.label_filename)
        self.filename_input = QLineEdit(self)
        random_number = random.randint(1000, 9999)
        self.filename_input.setText(f"qr-code-{random_number}")
        layout.addWidget(self.filename_input)

        # Кнопки для сохранения и открытия QR-кода
        self.save_button = QPushButton("Сохранить", self)
        self.save_button.setStyleSheet(self.button_style)
        self.save_button.clicked.connect(self.make_qr_code)
        layout.addWidget(self.save_button)

        self.show_button = QPushButton("Открыть", self)
        self.show_button.setStyleSheet(self.button_style)
        self.show_button.clicked.connect(self.show_qr_code)
        layout.addWidget(self.show_button)

        # Установка общего макета
        self.setLayout(layout)

    def make_qr_code(self):
        # Получаем параметры из пользовательского ввода
        text = self.text_input.text()
        size = int(self.size_input.text())
        level = self.level_input.value()
        color = self.color_input.currentText().lower()
        bg_color = self.bg_color_input.currentText().lower()

        # Преобразование цвета для фона в PyQt5
        color_map = {
            "black": "black",
            "red": "red",
            "blue": "blue",
            "green": "green",
            "purple": "#800080",
            "teal": "#008080",
            "white": "white",
            "light yellow": "#ffffe0",
            "light pink": "#ffb6c1",
            "light blue": "#add8e6",
            "mint": "#98ff98"
        }

        # Генерация QR-кода
        qr = qrcode.QRCode(version=level, box_size=size, border=5)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill=color_map[color], back_color=color_map[bg_color])

        # Сохранение QR-кода
        filename = self.filename_input.text()
        img.save(f"{filename}.png")
        QMessageBox.information(self, "Успех", f"Файл '{filename}.png' успешно сохранён!")

    def show_qr_code(self):
        # Показ изображения QR-кода
        filename = self.filename_input.text() + ".png"
        try:
            img = Image.open(filename)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", "Файл не найден!")

# Запуск приложения
app = QApplication([])
window = QRCodeGenerator()
window.show()
app.exec_()
