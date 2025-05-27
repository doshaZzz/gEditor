import json
from PyQt6.QtWidgets import QGraphicsScene
from shapes.shape import Shape

class Saver:
    def __init__(self, scene: QGraphicsScene):
        self.scene = scene
    
    def to_json(self):
        items_data = []
        seen = set()
        for item in self.scene.items():
            if not isinstance(item, Shape) or item in seen:
                continue
            # пропускаем дочерние элементы групп
            if item.parentItem() is not None:
                continue
            try:
                item_dict = item.to_dict()
                items_data.append(item_dict)
            except Exception as e:
                print(f"Error capturing item {item}: {e}")
        return json.dumps(items_data, indent=2)


    @staticmethod
    def from_json(json_str):
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return []