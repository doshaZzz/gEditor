from shapes.shape import Shape
from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QPainter


class Rectangle(Shape):
    """Класс для прямоугольника. В классе Rectangle рисуем прямоугольник через метод drawRect()."""
    def __init__(self):
        super().__init__()  # Важно: вызываем конструктор родительского класса Shape
    
    def boundingRect(self) ->  QRectF:
        return QRectF(50,50,50,50)
    
    def paint(self, painter: QPainter, option, widget=...):
        rect = QRectF(50,50,50,50)
        return painter.drawRect(rect)  # Рисуем прямоугольник