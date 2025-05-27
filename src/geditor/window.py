import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QGraphicsScene, QToolBar, QMenu, QGraphicsView, QGraphicsEllipseItem, QGraphicsItemGroup, QGraphicsItem
from PyQt6.QtGui import QAction, QPainter
from shapes.groupShape import GroupShape
from shapes.shapeFactory import ShapeFactory
from shapes.typeShape import TypeShape
from tools.undoRedo import UndoRedo
from tools.delItem import Del


class MainScene(QGraphicsScene):
    def __init__(self, undo_redo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.undo_redo = undo_redo
        self._initial_positions = {}

    def mousePressEvent(self, event):
        # Запоминаем начальные позиции всех выделенных фигур
        self._initial_positions = {
            item: item.pos() for item in self.selectedItems()
        }
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        moved = False
        for item in self.selectedItems():
            old_pos = self._initial_positions.get(item)
            if old_pos is not None and item.pos() != old_pos:
                moved = True
                break

        if moved:
            self.undo_redo.push_state()

        super().mouseReleaseEvent(event)
        
        
# Подкласс QMainWindow для настройки главного окна приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
                       
        self.setWindowTitle("gEditor")
        self.resize(800,600)
        
        central = QWidget()        
        mainLayout = QVBoxLayout(central)
        
        #self.mainScene = QGraphicsScene()
        
        self.undo_redo = UndoRedo(None)  # Временно без сцены
        self.mainScene = MainScene(self.undo_redo)
        self.undo_redo.scene = self.mainScene  # Передаём сцену после инициализации

        
        # Подключаем сигнал изменения цвета выделения фигур
        self.mainScene.selectionChanged.connect(self.update_selection)
        self.mainScene.addText("")
        self.mainViewe = QGraphicsView(self.mainScene)
        self.mainViewe.setDragMode(QGraphicsView.DragMode.RubberBandDrag)  # Режим выделения с помощью прямоугольной рамки
        self.mainViewe.setRenderHint(QPainter.RenderHint.Antialiasing)     # Сглаживание
        #self.undo_redo = UndoRedo(self.mainScene)
        self.delItem = Del()
                
        self.menuBar().addMenu("Файл")
        self.menuBar().addMenu("Настройки")
        self.menuBar().addMenu("Сохранить")
        self.menuBar().addMenu("Загрузить")
        
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
        
        action11 = QAction("Rotate Triangle", self)
        action11.triggered.connect(self.add_rotate_triangle_triggered)
        toolbar.addAction(action11)
        
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
        
        
        mainLayout.addWidget(toolbar)
        mainLayout.addWidget(self.mainViewe)
        
        # Устанавливаем центральный виджет Window.
        central.setLayout(mainLayout)
        self.setCentralWidget(central)
        
        #squareAction = toolbar.addAction("Круг")
        #squareAction.setShortcut("Ctrl+O")
         
        # button = QPushButton("Press Me!")
        
        # button.setCheckable(True)
        
        # button.clicked.connect(self.the_button_was_clicked)
        
        # button.clicked.connect(self.the_button_was_toggled)
               
    # def the_button_was_clicked(self):
    #     print("Clicked!")
        
    # def the_button_was_toggled(self, checked):
    #     print("Checked?", checked)
    
    def update_selection(self):
        # self.undo_redo.push_state()  # Сохраняем состояние перед изменением
        # Принудительно обновляем сцену, чтобы перерисовать выделенные элементы
        self.mainScene.update()
        
    def del_item_triggered(self):
        Del.deleteItem(self.mainScene)
        self.undo_redo.push_state()  # Сохраняем состояние перед изменением
        
    def add_rectangle_triggered(self):
        currentShape = ShapeFactory()        
        self.mainScene.addItem(currentShape.factory_method(TypeShape.RECTANGLE))
        self.undo_redo.push_state()  # Сохраняем состояние перед изменением
        print("Квадрат нарисовае!")
        #self.undo_redo.push_state()  # Сохраняем состояние перед изменением
        
    def add_triangle_triggered(self):
        currentShape = ShapeFactory()        
        self.mainScene.addItem(currentShape.factory_method(TypeShape.TRIANGLE))
        self.undo_redo.push_state()  # Сохраняем состояние перед изменением
        print("Треугольник нарисовае!")
        #self.undo_redo.push_state()  # Сохраняем состояние перед изменением
        
    def add_rotate_triangle_triggered(self):
        currentShape = ShapeFactory()        
        self.mainScene.addItem(currentShape.factory_method(TypeShape.ROTATE_TRIANGLE))
        self.undo_redo.push_state()  # Сохраняем состояние перед изменением
        print("Вращающийся треугольник нарисовае!")
        #self.undo_redo.push_state()  # Сохраняем состояние перед изменением
        
    def add_circle_triggered(self):
        currentShape = ShapeFactory()        
        self.mainScene.addItem(currentShape.factory_method(TypeShape.CIRCLE))
        print("Круг нарисовае!")
        self.undo_redo.push_state()  # Сохраняем состояние перед изменением
        
    def rotate_item_left(self):
        selected_items = self.mainScene.selectedItems()
        for item in selected_items:
            if hasattr(item, 'rotationItem'):
                item.rotationItem("left")
        self.undo_redo.push_state()  # Сохраняем состояние после вращения
        
    def rotate_item_right(self):
        selected_items = self.mainScene.selectedItems()
        for item in selected_items:
            if hasattr(item, 'rotationItem'):
                item.rotationItem("right")
        self.undo_redo.push_state()  # Сохраняем состояние после вращения
        
    def add_groupe_triggered(self):
        self.undo_redo.push_state()  # <--- Сохраняем СЦЕНУ до группировки!
        selected_items = self.mainScene.selectedItems()
        
        if len(selected_items) > 1:
            group = GroupShape()  # Используем наш класс GroupShape
            
            for item in selected_items:
                item.setSelected(False)
                self.mainScene.removeItem(item)
                group.addToGroup(item)
            
            self.mainScene.addItem(group)
            group.setSelected(True)
            print("Фигуры сгруппированы!")
        #self.undo_redo.push_state()  # Сохраняем состояние перед изменением
            
    def add_ungroupe_triggered(self):
        selected_items = self.mainScene.selectedItems() # Получаем все выделенные элементы
        for item in selected_items:
            # Проверяем, является ли элемент группой
            if isinstance(item, QGraphicsItemGroup): # isinstance используется для проверки принадлежности объекта к определённому классу или кортежу классов                
                #group_pos = item.scenePos() # Запоминаем позицию группы                
                children = item.childItems() # Получаем все дочерние элементы группы                            
                self.mainScene.removeItem(item) # Удаляем группу со сцены
                #self.mainScene.destroyItemGroup(item) # Разгруппировка
                for child in children: # Восстанавливаем элементы с учетом позиции группы
                    child.setPos(child.scenePos())  # Сохраняем абсолютную позицию
                    self.mainScene.addItem(child)
                    child.setSelected(True)
        self.undo_redo.push_state()  # Сохраняем состояние перед изменением
            