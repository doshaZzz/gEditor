from PyQt6.QtCore import QPropertyAnimation, QTimer, pyqtProperty, QObject
from PyQt6.QtGui import QVector3D
from PyQt6.QtWidgets import QGraphicsRotation, QGraphicsItem


class RotationWrapper(QObject):
    def __init__(self, item: QGraphicsItem):
        super().__init__()
        self._item = item
        self._angle = 0

    @pyqtProperty(float) # Cвойство для анимации
    def angle(self):
        return self._angle # Возвращаем текущий угол

    @angle.setter # Метод установки значения для свойства
    def angle(self, value):
        self._angle = value # Устанавливаем новый угол
        # Применяем вращение к графическому элементу
        self._item.rotation.setAngle(self._angle)
        self._item.setTransformations([self._item.rotation])
        self._item.update()

def auto_rotate(cls):
    """Декоратор для автоматического вращения фигур"""
    class AutoRotatingShape(cls):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs) # Инициализация базовой фигуры
            self._rotation_wrapper = RotationWrapper(self)
            self._setup_animation()
        
        def _setup_animation(self):
             # Анимация для свойства angle обертки
             # Ищет свойство с указанным именем (angle) и автоматически вызывает сеттер при изменении значения
            self._anim = QPropertyAnimation(self._rotation_wrapper, b"angle")
            self._anim.setDuration(2000)  # 2 секунды на полный оборот
            self._anim.setStartValue(0)
            self._anim.setEndValue(360)
            self._anim.setLoopCount(-1)  # Бесконечное повторение
            self._anim.start()
            
        def stop_rotation(self):
            self._anim.stop()
            
        def set_rotation_speed(self, speed_ms):
            self._anim.setDuration(speed_ms)
            
    return AutoRotatingShape