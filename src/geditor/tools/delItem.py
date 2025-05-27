from PyQt6.QtWidgets import QGraphicsScene, QGraphicsItemGroup, QGraphicsItem

class Del:
    def __init__(self):
        self.scene = None
    
    @staticmethod
    def deleteItem(scene: QGraphicsScene):
        selected_items = scene.selectedItems()    
        # Remove each selected item
        for item in selected_items:
            scene.removeItem(item)
