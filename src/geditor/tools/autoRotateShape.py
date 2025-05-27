from PyQt6.QtCore import QPropertyAnimation, QTimer, pyqtProperty, QObject
from PyQt6.QtGui import QVector3D
from PyQt6.QtWidgets import QGraphicsRotation, QGraphicsItem
from shapes.groupShape import GroupShape

class RotationWrapper(QObject):
    def __init__(self, item: QGraphicsItem):
        super().__init__()
        self._item = item
        self._angle = 0
        self._anim = None

    @pyqtProperty(float)
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):

        self._angle = value
        try:
            if isinstance(self._item, GroupShape):
                # Для GroupShape используем его собственный метод поворота
                self._item._current_angle = self._angle
                self._item.update_rotation_center()  # Обновляем центр вращения
                self._item.group_rotation.setAngle(self._angle)
                self._item.setTransformations([self._item.group_rotation])
            else:
                    # Для других элементов создаем новый QGraphicsRotation    
                if not hasattr(self._item, 'rotation') or self._item.rotation is None:
                    self._item.rotation = QGraphicsRotation()           
                center = self._item.boundingRect().center()
                self._item.rotation.setOrigin(QVector3D(center.x(), center.y(), 0))
                self._item.rotation.setAngle(self._angle)
                self._item.setTransformations([self._item.rotation])
            self._item.update()
        except RuntimeError as e:
            print(f"RotationWrapper.angle setter error: {e}")
            self._item.rotation = None

def auto_rotate(cls):
    """Декоратор для автоматического вращения фигур"""
    class AutoRotatingShape(cls):
        def __init__(self, *args, children=None, **kwargs):
            super().__init__(*args, **kwargs)
            self._rotation_wrapper = RotationWrapper(self)
            self._anim = None
            self._is_rotating = False
            if children and isinstance(self, GroupShape): 
                for child in children: 
                    self.addToGroup(child) 
                self.updateBoundingRect() 
        
        def __del__(self):
            if hasattr(self, '_anim') and self._anim:
                self._anim.stop()
        
        def _setup_animation(self):
            if not self._anim:
                self._anim = QPropertyAnimation(self._rotation_wrapper, b"angle")
                self._anim.setDuration(2000)
                self._anim.setStartValue(0)
                self._anim.setEndValue(360)
                self._anim.setLoopCount(-1)
        
        def toggle_rotation(self):
            self._setup_animation()
            if self._is_rotating:
                self._anim.stop()
                self._is_rotating = False
            else:
                self._anim.start()
                self._is_rotating = True
        
        def set_rotation_speed(self, speed_ms):
            self._setup_animation()
            self._anim.setDuration(speed_ms)
            
        def to_dict(self):
            base_dict = super().to_dict()
            base_dict['animation_duration'] = self._anim.duration() if self._anim else 2000
            base_dict['animation_running'] = self._is_rotating
            return base_dict
            
    return AutoRotatingShape