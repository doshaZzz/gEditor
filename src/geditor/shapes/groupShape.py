from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsItem, QGraphicsRotation, QGraphicsScene
from typing import Dict, List
from PyQt6.QtGui import QVector3D, QPainter
from shapes.shape import Shape
from PyQt6.QtCore import QRectF, QTimer
from shapes.typeShape import TypeShape
from PyQt6.QtCore import Qt

class GroupShape(Shape):
    def __init__(self):
        super().__init__()
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable | 
                     QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setAcceptHoverEvents(True)
        
        self._children: List[Shape] = []
        self._bounding_rect = QRectF()
        
        self._current_angle = 0
        self.group_rotation = QGraphicsRotation()
        self.rotation = self.group_rotation
        self.group_rotation.setAxis(QVector3D(0, 0, 1))
        self.setTransformations([self.group_rotation])
        
    def addToGroup(self, item: Shape):
        item.setParentItem(self)
        item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
        self._children.append(item)
        self.updateBoundingRect()
        self.update()
        
    def ungroup(self, scene):
        self.scene = scene
        selected_items = self.scene.selectedItems()
        for item in selected_items:
            if isinstance(item, GroupShape):
                group_pos = item.pos()
                children = item._children.copy()  # это настоящие дети
                self.scene.removeItem(item)

                for child in children:
                    child.setParentItem(None)
                    abs_x = group_pos.x() + child.x()
                    abs_y = group_pos.y() + child.y()
                    child.setPos(abs_x, abs_y)
                    child.setVisible(True)
                    child.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
                    child.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
                    self.scene.addItem(child)

                self.scene.clearSelection()
                print("Фигуры разгруппированы!")


    def updateBoundingRect(self):
        self.prepareGeometryChange()
        if not self._children:
            self._bounding_rect = QRectF(0, 0, 1, 1)
        else:
            rects = [child.mapRectToParent(child.boundingRect()) for child in self._children]
            self._bounding_rect = rects[0]
            for r in rects[1:]:
                self._bounding_rect = self._bounding_rect.united(r)

    def boundingRect(self) -> QRectF:
        return self._bounding_rect

    def paint(self, painter: QPainter, option, widget=None):
        if self.isSelected():
            painter.setPen(Qt.GlobalColor.blue)
            painter.setOpacity(0.2)
            painter.drawRect(self._bounding_rect)

    def rotationItem(self, direction: str):
        # Обновляем центр поворота каждый раз перед поворотом
        group_center = self.boundingRect().center()
        self.group_rotation.setOrigin(QVector3D(group_center.x(), group_center.y(), 0))

        if direction == "left":
            self._current_angle -= 30
        elif direction == "right":
            self._current_angle += 30
        else:
            print("Неизвестное направление")
            return

        self.group_rotation.setAngle(self._current_angle)
        self.setTransformations([self.group_rotation])
        self.update()

    def to_dict(self) -> Dict:
        items_data = []
        for item in self._children:
            item_data = item.to_dict()
            item_data['relative_x'] = item.x()
            item_data['relative_y'] = item.y()
            items_data.append(item_data)

        return {
            'type': TypeShape.GROUP.name,
            'x': self.x(),
            'y': self.y(),
            'rotation': self._current_angle,
            'z_value': self.zValue(),
            'items': items_data
        }

    def setPosFromDict(self, x: float, y: float):
        self.setX(x)
        self.setY(y)

    def update_rotation_center(self):
        group_center = self.boundingRect().center()
        self.group_rotation.setOrigin(QVector3D(group_center.x(), group_center.y(), 0))
        
    def removeFromGroup(self, item: Shape):
        if item in self._children:
            self._children.remove(item)
            item.setParentItem(None)
            item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            item.update()
            self.updateBoundingRect()

