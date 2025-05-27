from PyQt6.QtWidgets import QGraphicsScene, QGraphicsItemGroup
import json
from typing import Dict, List
from shapes.groupShape import GroupShape


class Saver:
    def __init__(self, scene: QGraphicsScene):
        self.scene_data = self._capture_scene(scene)
    
    def _capture_scene(self, scene: QGraphicsScene) -> List[Dict]:
        """Создает JSON-представление сцены"""
        items_data = []
        for item in scene.items():
            # Пропускаем элементы, которые уже в группах
            if item.parentItem() is not None:
                continue
            # Сохраняем группы (включая вложенные)
            if isinstance(item, QGraphicsItemGroup) and hasattr(item, 'to_dict'):
                items_data.append(item.to_dict())
            elif hasattr(item, 'to_dict'):
                items_data.append(item.to_dict())
        return items_data
    
    def to_json(self) -> str:
        """Возвращает JSON-строку"""
        return json.dumps(self.scene_data, indent=2)
    
    @staticmethod
    def from_json(json_str: str) -> List[Dict]:
        """Создает данные сцены из JSON"""
        return json.loads(json_str)
        
    
        
        