from PyQt6.QtWidgets import QApplication, QWidget

import sys # Только для доступа к аргументам командной строки

from window import MainWindow

# Приложению нужен один (и только один) экземпляр QApplication.
# Передаём sys.argv, чтобы разрешить аргументы командной строки для приложения.
# Если не будете использовать аргументы командной строки, QApplication([]) тоже работает
app = QApplication(sys.argv)

# Создаём виджет Qt — окно.
window = MainWindow()

window.show()  # Важно: окно по умолчанию скрыто.

# Запускаем цикл событий.
app.exec()


# Приложение не доберётся сюда, пока вы не выйдете и цикл
# событий не остановится.