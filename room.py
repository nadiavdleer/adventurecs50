# room.py
#
# Minor programmeren
# Nadia van der Leer
#
# - Room class file
# - collects descriptions, items and connections from rooms

class Room:
    def __init__(self, number, name, long_location):
        self._number = number
        self._long_location = long_location
        self.name = name
        self.flag = False
        self.connection = {}
        self.forced = False
        self.dict_items = {}
        self.conditional_connection = {}
        self.items_needed = {}

    # sets a room's status to visited after being there
    def set_visited(self):
        if self.flag == False and self.forced == False:
            self.flag = True

    # returns description of the room, depending on visited or not
    def description(self):
        if self.forced == True or self.flag == False:
            return f"{self._long_location}"
        elif self.flag == True:
            return f"{self.name}"

    # method to always return long description
    def long_description(self):
        return f"{self._long_location}"

    # add connections to rooms through loader.py
    def add_connection(self, direction, room_object):
        self.connection[direction] = room_object
        if direction == "FORCED":
            self.forced = True

    # add conditional connections
    def add_conditional_connection(self, direction, room_object):
        self.conditional_connection[direction] = room_object

    # check if room has certain connection(s)
    def has_connection(self, direction):
        if direction in self.connection:
            return True
        else:
            return False

    # execute a movement
    def get_connection(self, direction):
        if direction in self.connection:
            return self.connection[direction]

    # checks if room has conditional connection(s)
    def has_conditional_connection(self, direction):
        if direction in self.conditional_connection:
            return True
        else:
            return False

    # execute a conditonal movement
    def get_conditional_connection(self, direction):
        if direction in self.conditional_connection:
            return self.conditional_connection[direction]

    # checks if room has items in it
    def has_item(self):
        if len(self.dict_items) == 0:
            return False
        else:
            return True

    # returns all items that are in a room
    def all_items_room(self):
        if self.has_item:
            return self.dict_items

