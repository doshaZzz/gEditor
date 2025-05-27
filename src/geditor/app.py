from PyQt6.QtWidgets import QApplication, QWidget
import sys
from window import MainWindow

# Передаём sys.argv, чтобы разрешить аргументы командной строки для приложения.
# Если не будете использовать аргументы командной строки, QApplication([]) тоже работает
app = QApplication(sys.argv)

window = MainWindow()

window.show()

# Запускаем цикл событий.
app.exec()

