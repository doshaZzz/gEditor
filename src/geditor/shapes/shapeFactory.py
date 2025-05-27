from shapes.rectangle import Rectangle
from shapes.circle import Circle
from shapes.triangle import Triangle, RotatingTriangle
from .typeShape import TypeShape
from shapes.groupShape import GroupShape
    

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
        
        if shape_type == TypeShape.CIRCLE:
            return Circle()
        
        if shape_type == TypeShape.TRIANGLE:
            return Triangle()
        
        if shape_type == TypeShape.ROTATE_TRIANGLE:
            return RotatingTriangle()
        
        if shape_type == TypeShape.GROUP:
            return GroupShape() 
        
        else:
            raise ValueError(f"Unknown shape type: {shape_type}")
        
