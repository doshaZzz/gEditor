from typing import Dict, List
from PyQt6.QtWidgets import QGraphicsScene
from .saver import Saver
from shapes.rectangle import Rectangle
from shapes.circle import Circle
from shapes.shapeFactory import ShapeFactory
from shapes.typeShape import TypeShape
from PyQt6.QtGui import QPainter, QColor, QPen

class UndoRedo:
    def __init__(self, scene: QGraphicsScene):
        self.scene = scene
        self.undo_stack: List[Saver] = []
        self.redo_stack: List[Saver] = []
        self.max_stack_size = 20
    
    def push_state(self):
        """Сохраняет текущее состояние сцены"""
        if len(self.undo_stack) >= self.max_stack_size:
            self.undo_stack.pop(0)
        self.undo_stack.append(Saver(self.scene))
        self.redo_stack.clear()  # Очищаем redo при новом действии
    
    def undo(self):
        """Откатывает последнее действие"""
        if not self.undo_stack: # Проверяет, пуст ли стек
            return
        
        current_state = Saver(self.scene)
        self.redo_stack.append(current_state)
        
        # Восстанавливаем предыдущее состояние
        prev_state = self.undo_stack.pop()
        self._restore_scene(prev_state.scene_data)
    
    def redo(self):
        """Повторяет отмененное действие"""
        if not self.redo_stack:
            return
        
        current_state = Saver(self.scene)
        self.undo_stack.append(current_state)
        
        # Восстанавливаем следующее состояние
        next_state = self.redo_stack.pop()
        self._restore_scene(next_state.scene_data)
    
    def _restore_scene(self, scene_data: List[Dict]):
        
            """Восстанавливает сцену из данных"""
            self.scene.clear()
            factory = ShapeFactory()
            
            for item_data in scene_data:
                try:
                    # Преобразуем строку в enum
                    shape_type = TypeShape[item_data['type']]
                    
                    if shape_type == TypeShape.GROUP:
                        # Восстанавливаем группу
                        group = factory.factory_method(shape_type)
                        group.setPos(item_data['x'], item_data['y'])
                        
                        # Восстанавливаем элементы группы
                        for child_data in item_data['items']:
                            # Преобразуем строку в enum
                            child_type = TypeShape[child_data['type']]
                            child = factory.factory_method(child_type)
                            
                            if 'color' in child_data:
                                child.color = QColor(child_data['color'])
                            group.addToGroup(child)
                            child.setPos(child_data['x'], child_data['y'])
                        self.scene.addItem(group)
                    # Восстанавливаем обычные фигуры
                    else:
                        shape = factory.factory_method(shape_type)
                        # Устанавливаем параметры
                        shape.setPos(item_data['x'], item_data['y'])
                        if 'color' in item_data:
                            shape.color = QColor(item_data['color'])
                        if 'z_value' in item_data:
                            shape.setZValue(item_data['z_value'])
                        self.scene.addItem(shape)
                except KeyError as e:
                    print(f"Ошибка при восстановлении фигуры: {e}")
