# item.py
#
# Minor programmeren
# Nadia van der Leer
#
# - Item class file
# - returns taken and dropped statements

class Item:
    def __init__(self, name, description, item_room):
        self.name = name
        self.description = description
        self.item_room = item_room

    # convert into string
    def __str__(self):
        return f"{self.name}: {self.description}"

    # string for when item is taken, used in adventure.py
    def take(self):
        return f"{self.name} taken"

    # string for when item is dropped, used in adventure.py
    def drop(self):
        return f"{self.name} dropped"

