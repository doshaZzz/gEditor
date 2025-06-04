from PyQt6.QtWidgets import QGraphicsScene, QGraphicsItem
from shapes.shapeFactory import ShapeFactory
from tools.saver import Saver

class UndoRedo:
    def __init__(self, scene: QGraphicsScene):
        self.scene = scene
        self.states = [[]]  # Стек
        self.current_index = 0  # Указатель на текущее состояние
        self.saver = None

    def push_state(self):
        if self.saver is None:
            self.saver = Saver(self.scene)
        current_state = self.saver.to_json()
        current_state = self.saver.from_json(current_state)
        
        # Усекаем список до текущего индекса и добавляем новое состояние
        if self.current_index < len(self.states) - 1:
            self.states = self.states[:self.current_index + 1]
        self.states.append(current_state)
        self.current_index += 1
        print(f"Состояние: {self.states}, Текущий index: {self.current_index}")

    def undo(self):
        if self.current_index > 0:
            self.current_index -= 1
            self._restore_scene(self.states[self.current_index])
            print(f"Undo to index: {self.current_index}")

    def redo(self):
        if self.current_index < len(self.states) - 1:
            self.current_index += 1
            self._restore_scene(self.states[self.current_index])
            print(f"Redo to index: {self.current_index}")

    def _restore_scene(self, state):
        for item in self.scene.items():
            self.scene.removeItem(item)
        factory = ShapeFactory()
        for item_data in state:
            try:
                shape = factory.from_dict(item_data)
                self.scene.addItem(shape)
            except Exception as e:
                print(f"Error restoring item {item_data}: {e}")
        self.scene.update()

    def clear(self):
        """Очистка стека при сохранении или загрузке"""
        self.states = [[]]
        self.current_index = 0