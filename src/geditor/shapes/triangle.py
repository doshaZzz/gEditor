from PyQt6.QtCore import QPointF, QRectF, QPropertyAnimation
from PyQt6.QtGui import QPolygonF, QPainter, QColor, QPen
from typing import Dict
from shapes.shape import Shape
from shapes.typeShape import TypeShape
import random

class Triangle(Shape):
    def __init__(self, width=50, height=50):
        super().__init__()
        self.width = width
        self.height = height
        x = random.uniform(0, 400)
        y = random.uniform(0, 400)
        # Определяем вершины треугольника относительно локального начала координат
        self._points = [
            QPointF(0, height),           # Нижняя левая вершина
            QPointF(width / 2, 0),        # Верхняя вершина
            QPointF(width, height)        # Нижняя правая вершина
        ]
        self._polygon = QPolygonF(self._points)
        self.setPos(x, y)  # Устанавливаем случайную позицию на сцене
        
    def boundingRect(self):
        # Возвращаем прямоугольник, охватывающий треугольник
        return QRectF(0, 0, self.width, self.height)
    
    def shape(self):
        # Возвращаем форму для точного определения области взаимодействия
        from PyQt6.QtGui import QPainterPath
        path = QPainterPath()
        path.addPolygon(self._polygon)
        return path
    
    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if self.isSelected():
            painter.setPen(self.selected_pen)
        else:
            painter.setPen(self.normal_pen)
        
        painter.setBrush(self.color)
        # Рисуем полигон в локальных координатах
        painter.drawPolygon(self._polygon)
    
    def to_dict(self) -> Dict:
        return {
            'type': TypeShape.TRIANGLE.name,
            'width': self.width,
            'height': self.height,
            'color': self.color.name(),
            'x': self.x(),
            'y': self.y(),
            'z_value': self.zValue(),
            'rotation': self._current_angle
        }
    
    def update_polygon(self):
        self._polygon = QPolygonF(self._points)
        self.update()