from shapes.rectangle import Rectangle
from shapes.circle import Circle
from shapes.triangle import Triangle #. RotatingTriangle
from shapes.groupShape import GroupShape
from shapes.typeShape import TypeShape
from tools.autoRotateShape import auto_rotate

class ShapeFactory:
    def factory_method(self, shape_type: TypeShape):
        if shape_type == TypeShape.RECTANGLE:
            return Rectangle()
        elif shape_type == TypeShape.CIRCLE:
            return Circle()
        elif shape_type == TypeShape.TRIANGLE:
            return Triangle()
        elif shape_type == TypeShape.GROUP:
            return GroupShape()
        else:
            raise ValueError(f"Unknown shape type: {shape_type}")

    def from_dict(self, data: dict):
        
        shape_type = data.get('type')
        animation_running = data.get('animation_running')
        
        if shape_type == TypeShape.RECTANGLE.name:
            if animation_running == True:
                # Создаём класс с анимацией
                AnimatedRect = auto_rotate(Rectangle)
                shape = AnimatedRect()  # создаём экземпляр класса с анимацией
                shape.setPos(data['x'], data['y'])
                shape.setZValue(data['z_value'])
                shape.toggle_rotation()  # запускаем анимацию
            else:
                shape = Rectangle()
                shape.setPos(data['x'], data['y'])
                shape.setZValue(data['z_value'])
            return shape
        
        elif shape_type == TypeShape.CIRCLE.name:
            shape = Circle()            
            # Восстановим радиус
            radius = data['radius']
            shape.set_radius(radius)
            # Восстановим поворот
            shape.setRotation(data.get('rotation', 0))                        
            shape.setPos(data['x'], data['y'])
            shape.setZValue(data['z_value'])
            return shape
        
        elif shape_type == TypeShape.TRIANGLE.name:
            # Если анимация нужна — создаём обёрнутый класс
            if animation_running == True:
                # Создаём класс с анимацией
                AnimatedTriangle = auto_rotate(Triangle)
                shape = AnimatedTriangle()  # создаём экземпляр класса с анимацией
                shape.setPos(data['x'], data['y'])
                shape.setZValue(data['z_value'])
                shape.toggle_rotation()  # запускаем анимацию
            else:
                shape = Triangle()
                shape.setPos(data['x'], data['y'])
                shape.setZValue(data['z_value'])
            return shape
        
        elif shape_type == TypeShape.GROUP.name:
            if animation_running == True:
                # Создаём класс с анимацией
                AnimatedGroup = auto_rotate(GroupShape)
                shape = AnimatedGroup()
                shape.setPos(data['x'], data['y'])
                shape.setZValue(data['z_value'])
                for item_data in data.get('items', []):
                    child = self.from_dict(item_data)
                    child.setPos(item_data['relative_x'], item_data['relative_y'])
                    shape.addToGroup(child)
                print("Toggle rotation called")
                shape.toggle_rotation()  # запускаем анимацию
                print("Rotation toggled")
                print(f"Group children count: {len(shape._children)}")
                print(f"Group boundingRect: {shape.boundingRect()}")
            else:
                shape = GroupShape()
                shape.setPos(data['x'], data['y'])
                shape.setZValue(data['z_value'])
                for item_data in data.get('items', []):
                    child = self.from_dict(item_data)
                    child.setPos(item_data['relative_x'], item_data['relative_y'])
                    shape.addToGroup(child)
            return shape
        else:
            raise ValueError(f"Unknown shape type: {shape_type}")