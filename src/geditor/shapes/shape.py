from PyQt6.QtWidgets import QGraphicsItem
from abc import ABC, abstractmethod, ABCMeta
from PyQt6.QtGui import QPainter, QColor

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

    @abstractmethod    
    def boundingRect(self):
        pass
    
    @abstractmethod  
    def paint(self, painter: QPainter, option, widget = ...):
        pass
        
    
        
