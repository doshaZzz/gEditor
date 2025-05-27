from shapes.shape import Shape
from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QGraphicsEllipseItem
from typing import Dict
from .typeShape import TypeShape


class Circle(Shape):
    """Класс для круга. В классе Circle рисуем круг через метод drawElips()."""
    def __init__(self):
        super().__init__()  # Важно: вызываем конструктор родительского класса Shape
        self.elips = QRectF(200,0,50,50)
    
    def boundingRect(self) ->  QRectF:
        return self.elips
    
    def paint(self, painter: QPainter, option, widget=...):
        super().paint(painter, option, widget)  # Вызываем родительский метод для установки пера
        return painter.drawEllipse(self.elips)  # Рисуем круг
    
    def to_dict(self) -> Dict:
        return {
            'type': "CIRCLE",
            'x': self.x(),
            'y': self.y(),
            'radius': self.elips.width()/2,
            'color': self.color.name(),
            'z_value': self.zValue() # Значение определяет порядок наложения родственных (соседних) элементов.
        } 