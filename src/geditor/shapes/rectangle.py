from shapes.shape import Shape
from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QPainter
from typing import Dict
from .typeShape import TypeShape
import random


class Rectangle(Shape):
    """Класс для прямоугольника. В классе Rectangle рисуем прямоугольник через метод drawRect()."""
    def __init__(self):
        super().__init__()  # вызываем конструктор родительского класса Shape
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        self.width = 50
        self.height = 50
        # Центрируем прямоугольник
        self.rect = QRectF(-self.width/2, -self.height/2, self.width, self.height)
        #self.setPos(x, y)  # Устанавливаем случайную позицию
    
    def boundingRect(self) ->  QRectF:
        return self.rect
    
    def paint(self, painter: QPainter, option, widget=...):
        super().paint(painter, option, widget)  # Вызываем родительский метод для установки пера
        return painter.drawRect(self.rect)  # Рисуем прямоугольник
    
    def to_dict(self) -> Dict:
        return {
            'type': TypeShape.RECTANGLE.name,
            'x': self.x(),
            'y': self.y(),
            'width': self.rect.width(),
            'height': self.rect.height(),
            'color': self.color.name(),
            'z_value': self.zValue(), # Значение определяет порядок наложения родственных (соседних) элементов.
            'rotation': self._current_angle
        }