from enum import Enum
from shapes.rectangle import Rectangle

class TypeShape(Enum) :
    """Типы фигур"""
    RECTANGLE = 1
    CIRCLE = 2
    TRIANGLE = 3
    ### todo: Добавить остальные фигуры сюда
    

class ShapeFactory:
    def __init__(self):
        pass 
    
    def factory_method(self, shape_type: TypeShape):
        """
        Фабричный метод для создания объектов фигур
        
        :param shape_type: Тип фигуры из перечисления TypeShape
        :return: Объект соответствующей фигуры
        """
        if shape_type == TypeShape.RECTANGLE:
            return Rectangle()
                
        ### todo: Добавить остальные фигуры сюда
        else:
            raise ValueError(f"Unknown shape type: {shape_type}")
        
