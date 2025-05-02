import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QGraphicsScene, QToolBar, QMenu, QGraphicsView
from PyQt6.QtGui import QAction, QPainter
from shapes.shapeFactory import ShapeFactory, TypeShape

# Подкласс QMainWindow для настройки главного окна приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("gEditor")
        self.resize(800,600)
        
        central = QWidget()        
        mainLayout = QVBoxLayout(central)
        
        self.mainScene = QGraphicsScene()
        self.mainScene.addText("Сцена")
        self.mainViewe = QGraphicsView(self.mainScene)
        self.mainViewe.setDragMode(QGraphicsView.DragMode.RubberBandDrag)  # Режим выделения с помощью прямоугольной рамки
        self.mainViewe.setRenderHint(QPainter.RenderHint.Antialiasing)     # Сглаживание
        
        self.menuBar().addMenu("Файл")
        self.menuBar().addMenu("Настройки")
        self.menuBar().addMenu("Сохранить")
        self.menuBar().addMenu("Загрузить")
        
        toolbar = QToolBar("Main toolbar")
        self.addToolBar(toolbar)
        
        action1 = QAction("Rectangle", self)
        action1.triggered.connect(self.add_rectangle_triggered)
        toolbar.addAction(action1)
        
        action2 = QAction("Действие 2", self)
        toolbar.addAction(action2)
        
        action3 = QAction("Действие 3", self)
        toolbar.addAction(action3)
        
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
        
    def add_rectangle_triggered(self):
        currentShape = ShapeFactory()        
        self.mainScene.addItem(currentShape.factory_method(TypeShape.RECTANGLE))
        print("Квадрат нарисовае!")
