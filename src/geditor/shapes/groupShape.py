from PyQt6.QtWidgets import QGraphicsItemGroup ,QGraphicsItem, QGraphicsRotation
from typing import Dict
from PyQt6.QtGui import QVector3D

class GroupShape(QGraphicsItemGroup):
    def __init__(self):
        super().__init__()
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable | 
                     QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self._current_angle = 0  # Текущий угол вращения группы
        self.group_rotation = QGraphicsRotation()
        self.group_rotation.setAxis(QVector3D(0, 0, 1))  # Z-ось для 2D вращения

    def rotationItem(self, direction: str):
        # Вычисляем центр всей группы
        group_center = self.boundingRect().center()
        self.group_rotation.setOrigin(QVector3D(group_center.x(), group_center.y(), 0))
        
        # Изменяем угол в зависимости от направления
        if direction == "left":
            self._current_angle -= 30
        elif direction == "right":
            self._current_angle += 30
        else:
            print("Неизвестное направление")
            return
        
        # Устанавливаем новый угол для всей группы
        self.group_rotation.setAngle(self._current_angle)
        
        # Применяем преобразование ко всей группе
        self.setTransformations([self.group_rotation])
        self.update()  # Обновляем отображение
    
    def to_dict(self) -> Dict:
        """Сериализует группу и все её элементы"""
        items_data = []
        for item in self.childItems():
            if hasattr(item, 'to_dict'):
                item_dict = item.to_dict()
                # Сохраняем относительные координаты внутри группы
                item_dict['x'] = item.x()
                item_dict['y'] = item.y()
                items_data.append(item_dict)
        
        return {
            'type': "GROUP",
            'x': self.x(),  # Позиция группы на сцене
            'y': self.y(),
            'items': items_data,
            'z_value': self.zValue()
        }
        
        