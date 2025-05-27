from PyQt6.QtWidgets import QApplication, QWidget
import sys
from window import MainWindow

app = QApplication(sys.argv)

window = MainWindow()

window.show()

app.exec()

