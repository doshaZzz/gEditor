from PyQt6.QtWidgets import QGraphicsItem, QGraphicsRotation
from abc import ABC, abstractmethod, ABCMeta
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtCore import Qt, QPointF
from typing import Dict
from PyQt6.QtGui import QVector3D


class ShapeMeta(type(QGraphicsItem), ABCMeta):
    """Метакласс для объединения метаклассов QGraphicsItem и ABC."""
    pass

class Shape(QGraphicsItem, ABC, metaclass=ShapeMeta):
    """Абстрактный базовый класс для всех фигур."""
    def __init__(self):
        super().__init__()
        self.color = QColor("#000000")
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable | 
                      QGraphicsItem.GraphicsItemFlag.ItemIsMovable)  # Фигуры можно выделять и двигать
        self.normal_pen = QPen(Qt.GlobalColor.black, 2)  # Обычная черная обводка
        self.selected_pen = QPen(Qt.GlobalColor.red, 3)   # Красная обводка при выделении
        self._current_angle = 0  # Текущий угол вращения
        self.rotation = QGraphicsRotation()
        self.rotation.setAxis(QVector3D(0, 0, 1))  # Z-ось для 2D вращения

    def rotationItem(self, direction: str):
        # Получаем центр фигуры
        center = self.boundingRect().center()
        self.rotation.setOrigin(QVector3D(center.x(), center.y(), 0))  # Z=0 для 2D
        
        # Изменяем угол в зависимости от направления
        if direction == "left":
            self._current_angle -= 30
        elif direction == "right":
            self._current_angle += 30
        else:
            print("Неизвестное направление")
            return
        
        # Устанавливаем новый угол
        self.rotation.setAngle(self._current_angle)
        
        # Применяем преобразование
        self.setTransformations([self.rotation])
        self.update()  # Обновляем отображение     
    
    @abstractmethod    
    def boundingRect(self):
        pass
    
    @abstractmethod  
    def paint(self, painter: QPainter, option, widget = ...):
        # Устанавливаем кисть в зависимости от состояния выделения
        if self.isSelected():
            painter.setPen(self.selected_pen)
        else:
            painter.setPen(self.normal_pen)
     
    @abstractmethod       
    def to_dict(self) -> Dict:
        pass
        
    
        
