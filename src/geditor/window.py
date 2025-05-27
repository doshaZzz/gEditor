import sys
from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QGraphicsScene, QToolBar, QMenu, QGraphicsView, QGraphicsEllipseItem, QGraphicsItemGroup, QGraphicsItem
from PyQt6.QtGui import QAction, QPainter
from shapes.groupShape import GroupShape
from shapes.shapeFactory import ShapeFactory
from shapes.typeShape import TypeShape
from tools.undoRedo import UndoRedo
from tools.delItem import Del
from tools.saver import Saver
from tools.autoRotateShape import auto_rotate


class MainScene(QGraphicsScene):
    def __init__(self, undo_redo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.undo_redo = undo_redo
        self._initial_positions = {}
        # Подключите сигнал selectionChanged к методу
        self.selectionChanged.connect(self.on_selection_changed)

    def on_selection_changed(self):
        print(f"Выбор изменен: {[str(item) for item in self.selectedItems()]}")
        print(f"Элементы сцены: {[str(item) for item in self.items()]}")

    def mousePressEvent(self, event):
        self._initial_positions = {item: item.pos() for item in self.selectedItems()}
        super().mousePressEvent(event)

    # def mouseReleaseEvent(self, event):
    #     moved = False
    #     for item in self.selectedItems():
    #         old_pos = self._initial_positions.get(item)
    #         if old_pos is not None and item.pos() != old_pos:
    #             moved = True
    #             break
    #     if moved:
    #         self.undo_redo.push_state()
    #     super().mouseReleaseEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("gEditor")
        self.resize(800, 600)
        
        central = QWidget()
        mainLayout = QVBoxLayout(central)
        
        self.undo_redo = UndoRedo(None)
        self.mainScene = MainScene(self.undo_redo)
        self.undo_redo.scene = self.mainScene
        
        self.mainScene.selectionChanged.connect(self.update_selection)
        self.mainViewe = QGraphicsView(self.mainScene)
        self.mainViewe.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.mainViewe.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.delItem = Del()
                
        toolbar = QToolBar("Main toolbar")
        self.addToolBar(toolbar)
        
        action1 = QAction("Rectangle", self)
        action1.triggered.connect(self.add_rectangle_triggered)
        toolbar.addAction(action1)
        
        action2 = QAction("Circle", self)
        action2.triggered.connect(self.add_circle_triggered)
        toolbar.addAction(action2)
        
        action10 = QAction("Triangle", self)
        action10.triggered.connect(self.add_triangle_triggered)
        toolbar.addAction(action10)
                
        action3 = QAction("Group", self)
        action3.triggered.connect(self.add_groupe_triggered)
        toolbar.addAction(action3)
        
        action4 = QAction("Ungroup", self)
        action4.triggered.connect(self.add_ungroupe_triggered)
        toolbar.addAction(action4)
        
        action5 = QAction("<-- Undo", self)
        action5.setShortcut("Ctrl+Z")
        action5.triggered.connect(self.undo_redo.undo)
        toolbar.addAction(action5)
        
        action6 = QAction("Redo -->", self)
        action6.setShortcut("Ctrl+Y")
        action6.triggered.connect(self.undo_redo.redo)
        toolbar.addAction(action6)
        
        action7 = QAction("Delete Item", self)
        action7.setShortcut("del")
        action7.triggered.connect(self.del_item_triggered)
        toolbar.addAction(action7)
        
        action8 = QAction("Rotate left", self)
        action8.triggered.connect(self.rotate_item_left)
        toolbar.addAction(action8)
        
        action9 = QAction("Rotate right", self)
        action9.triggered.connect(self.rotate_item_right)
        toolbar.addAction(action9)
        
        action12 = QAction("Toggle Auto-Rotate", self)
        action12.triggered.connect(self.toggle_auto_rotate)
        toolbar.addAction(action12)
        
        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_scene_triggered)
        self.menuBar().addMenu("Сохранить").addAction(save_action)
        
        load_action = QAction("Load", self)
        load_action.triggered.connect(self.load_scene_triggered)
        self.menuBar().addMenu("Загрузить").addAction(load_action)
        
        mainLayout.addWidget(toolbar)
        mainLayout.addWidget(self.mainViewe)
        
        central.setLayout(mainLayout)
        self.setCentralWidget(central)
    
    def update_selection(self):
        if not self.mainScene:
            print("MainScene пуста, пропускаем update_selection")
            return
        print(f"Обновление выбранных элементов сцены. Элементы сцены: {[str(item) for item in self.mainScene.items()]}")
        self.mainScene.update()

    def del_item_triggered(self):        
        Del.deleteItem(self.mainScene)
        self.undo_redo.push_state()
        
    def add_rectangle_triggered(self):
        
        currentShape = ShapeFactory()
        shape = currentShape.factory_method(TypeShape.RECTANGLE)
        shape.setPos(100 + len(self.mainScene.items()) * 10, 100)  # Avoid overlap
        self.mainScene.addItem(shape)
        self.undo_redo.push_state()
        print("Квадрат нарисован!")
        
    def add_triangle_triggered(self): 
        currentShape = ShapeFactory()
        shape = currentShape.factory_method(TypeShape.TRIANGLE)
        shape.setPos(100 + len(self.mainScene.items()) * 10, 100)
        self.mainScene.addItem(shape)
        self.undo_redo.push_state()
        print("Треугольник нарисован!")
        
        
    def add_circle_triggered(self):
        
        currentShape = ShapeFactory()
        shape = currentShape.factory_method(TypeShape.CIRCLE)
        shape.setPos(100 + len(self.mainScene.items()) * 10, 100)
        self.mainScene.addItem(shape)
        self.undo_redo.push_state()
        print("Круг нарисован!")
        
    def rotate_item_left(self):
        selected_items = self.mainScene.selectedItems()
        for item in selected_items:
            if hasattr(item, 'rotationItem'):
                item.rotationItem("left")
        self.undo_redo.push_state()
        
    def rotate_item_right(self):
        selected_items = self.mainScene.selectedItems()
        for item in selected_items:
            if hasattr(item, 'rotationItem'):
                item.rotationItem("right")
        self.undo_redo.push_state()
        
    
    def toggle_auto_rotate(self):
        print("Старт toggle_auto_rotate")
        selected_items = self.mainScene.selectedItems()
        print(f"Выбранные элементы: {[type(item).__name__ for item in selected_items]}")
        for item in self.mainScene.selectedItems():
            print(f"Обработка элемента: {type(item).__name__}, toggle_rotation: {hasattr(item, 'toggle_rotation')}")
            if not hasattr(item, 'toggle_rotation'):
                # Применим декоратор вручную
                cls = auto_rotate(item.__class__)
                if isinstance(item, GroupShape): 
                    # Сохраняем дочерние элементы
                    children = item._children.copy() 
                    new_item = cls(children=children) 
                else: 
                    new_item = cls()
                print(f"Новая фигура создана: {type(new_item).__name__}, toggle_rotation: {hasattr(new_item, 'toggle_rotation')}")
                if not hasattr(new_item, 'toggle_rotation'):
                    raise RuntimeError(f"Не удалось создать анимированный элемент {type(new_item).__name__}")
                # Копируем позицию и цвет
                new_item.setPos(item.pos())
                if hasattr(item, 'color'):
                    new_item.color = item.color
                if hasattr(item, 'zValue'):  
                    new_item.setZValue(item.zValue()) 
                if hasattr(item, '_current_angle'): 
                    new_item._current_angle = item._current_angle
                self.mainScene.removeItem(item)
                self.mainScene.addItem(new_item)
                new_item.toggle_rotation()
                new_item.setSelected(True)
            else:
                # Если объект уже обернут декоратором, просто переключаем вращение
                print("Переключение существующего вращения")
                item.toggle_rotation()
        self.undo_redo.push_state()
        
    def add_groupe_triggered(self):
        selected_items = self.mainScene.selectedItems()
        if len(selected_items) > 1:
            group = GroupShape()
            min_x = min(item.scenePos().x() for item in selected_items)
            min_y = min(item.scenePos().y() for item in selected_items)
            group.setPos(min_x, min_y)
            print(f"Позиция группы: ({min_x}, {min_y})")
            for item in selected_items:
                item.setSelected(False)
                self.mainScene.removeItem(item)
                rel_x = item.scenePos().x() - min_x
                rel_y = item.scenePos().y() - min_y
                item.setPos(rel_x, rel_y)
                print(f"Child позиция: ({rel_x}, {rel_y})")
                group.addToGroup(item)
            group.update_rotation_center()
            self.mainScene.addItem(group)
            group.setSelected(True)
            self.undo_redo.push_state()
            print("Фигуры сгруппированы!")
            
    def add_ungroupe_triggered(self):
        selected_items = self.mainScene.selectedItems()
        changed = False
        # Откл selectionChanged для избежания преждевременных вызовов
        self.mainScene.selectionChanged.disconnect(self.update_selection)
        for item in selected_items:
            if isinstance(item, GroupShape):
                item.ungroup(self.mainScene)
                changed = True
        # Вкл selectionChanged
        self.mainScene.selectionChanged.connect(self.update_selection)
        if changed:
            print("Отправка состояния после разгруппировки")
            print(f"Элементы сцены до push_state: {[str(item) for item in self.mainScene.items()]}")
            QTimer.singleShot(100, self.undo_redo.push_state)

    def save_scene_triggered(self):
        saver = Saver(self.mainScene)
        with open('scene.json', 'w') as f:
            f.write(saver.to_json())
        self.undo_redo.clear()  # Очищаем стек
        print("Сцена сохранена!")

    def load_scene_triggered(self):
        try:
            with open('scene.json', 'r') as f:
                scene_data = Saver.from_json(f.read())
            if not scene_data:
                print("Нет данных для загрузки из scene.json")
                return
            self.undo_redo.clear()  # Очищаем стек
            self.undo_redo._restore_scene(scene_data)
            self.undo_redo.push_state()  # Добавляем новое состояние
            print("Сцена загружена!")
        except Exception as e:
            print(f"Ошибка загрузки сцены: {e}")