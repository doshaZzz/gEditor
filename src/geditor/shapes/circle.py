from shapes.shape import Shape
from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QGraphicsEllipseItem
from typing import Dict
from .typeShape import TypeShape
import random


class Circle(Shape):
    """Класс для круга. В классе Circle рисуем круг через метод drawElips()."""
    def __init__(self):
        super().__init__()  # Важно: вызываем конструктор родительского класса Shape
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        radius = 25
        self.elips = QRectF(-radius, -radius, radius * 2, radius * 2)  # Центр круга будет (0,0)
        self.setPos(x, y)  # Устанавливаем случайную позицию
    
    def boundingRect(self) ->  QRectF:
        return self.elips
    
    def set_radius(self, r: float):
        self.elips = QRectF(-r, -r, 2*r, 2*r)
    
    def paint(self, painter: QPainter, option, widget=...):
        super().paint(painter, option, widget)  # Вызываем родительский метод для установки пера
        return painter.drawEllipse(self.elips)  # Рисуем круг
    
    def to_dict(self) -> Dict:
        return {
            'type': TypeShape.CIRCLE.name,
            'x': self.x(),
            'y': self.y(),
            'radius': self.elips.width()/2,
            'color': self.color.name(),
            'z_value': self.zValue(), # Значение определяет порядок наложения родственных (соседних) элементов.
            'rotation': self._current_angle
        } 