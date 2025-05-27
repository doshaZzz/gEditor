from PyQt6.QtCore import QPointF, QRectF
from PyQt6.QtGui import QPolygonF
from PyQt6.QtGui import QPainter, QColor, QPen
from typing import Dict
from shapes.shape import Shape
from tools.autoRotateShape import auto_rotate

class Triangle(Shape):
    def __init__(self, width=50, height=50):
        super().__init__()
        self.width = width
        self.height = height
        self._points = [
            QPointF(0, height),          # Нижний левый угол
            QPointF(width/2, 0),         # Верхний центр
            QPointF(width, height)       # Нижний правый угол
        ]
        self._polygon = QPolygonF(self._points)
        
    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)
    
    def paint(self, painter: QPainter, option, widget=None):
        # Устанавливаем кисть в зависимости от состояния выделения
        if self.isSelected():
            painter.setPen(self.selected_pen)
        else:
            painter.setPen(self.normal_pen)
        
        painter.setBrush(self.color)
        painter.drawPolygon(self._polygon)
    
    def to_dict(self) -> Dict:
        return {
            'type': 'triangle',
            'width': self.width,
            'height': self.height,
            'color': self.color.name(),
            'position': {
                'x': self.pos().x(),
                'y': self.pos().y()
            },
            'rotation': self._current_angle
        }
    
    def update_polygon(self):
        """Обновляет полигон после трансформаций"""
        self._polygon = QPolygonF(self._points)
        self.update()

@auto_rotate
class RotatingTriangle(Triangle):
    """Треугольник с автоматическим вращением"""
    pass