# adventure.py
#
# Minor programmeren
# Nadia van der Leer
#
# - main game file
# - executes movements, statements, taking and dropping of items

import loader


class Adventure():

    # Create rooms and items for the game that was specified at the command line
    def __init__(self, filename):
        self._current_room = loader.load_room_graph(filename)
        self.inventory = {}
        self.synonyms = {}

    # Pass along the description of the current room, be it short or long
    def room_description(self):
        return self._current_room.description()

    # long room description for
    def room_long_des(self):
        return self._current_room.long_description()

    # Move to a different room by changing "current" room, if possible
    def move(self, direction):
        if self._current_room.has_connection(direction):
            destination_room = self._current_room.get_connection(direction)
            self._current_room.set_visited()
            self._current_room = destination_room
            return True
        else:
            return False

    # Move to a room with a conditional connection
    def conditional_move(self, direction):

        if self._current_room.has_conditional_connection(direction):
            self._current_room.set_visited()

            destination_room = self._current_room.get_conditional_connection(direction)
            if self._current_room.items_needed[destination_room] in self.inventory:
                self._current_room = destination_room
                return True
        else:
            return False

    # checks for forced connection
    def forced_connection(self):
        if self._current_room.has_connection("FORCED"):
            return True
        else:
            return False

    # checks for forced conditional connection
    def forced_conditional_connection(self):
        if self._current_room.has_conditional_connection("FORCED"):
            return True
        else:
            return False

    # returns dictionary of all items in room
    def item(self):
        return self._current_room.all_items_room()

    # checks if there are items in the room
    def item_present(self):
        if self._current_room.has_item():
            return True
        else:
            return False

    # takes item from the room
    def item_taken(self, item):
        if item in self._current_room.dict_items:
            self.inventory[item] = self._current_room.dict_items[item]
            del self._current_room.dict_items[item]
            return self.inventory[item].take()
        else:
            return "No such item"

    # drops item in a room
    def item_dropped(self, item):
        if item in self.inventory:
            self._current_room.dict_items[item] = self.inventory[item]
            dropped = self.inventory[item].drop()
            del self.inventory[item]
            return dropped
        else:
            return "No such item"

    # loads the synonyms file
    def load_synonyms(self):
        with open("data/Synonyms.dat") as file:
            for line in file:
                line = line.rstrip()
                syn_list = line.split("=")
                synonym = syn_list[0]
                word = syn_list[1]

                self.synonyms[synonym] = word


if __name__ == "__main__":

    from sys import argv

    # Check command line arguments
    if len(argv) not in [1, 2]:
        print("Usage: python3 adventure.py [name]")
        exit(1)

    # Load the requested game or else Tiny
    print("Loading...")
    if len(argv) == 2:
        game_name = argv[1]
    elif len(argv) == 1:
        game_name = "Tiny"
    filename = f"data/{game_name}Adv.dat"

    # Create game
    adventure = Adventure(filename)

    # Welcome user
    print("Welcome to Adventure.\n")

    # Print very first room description
    print(adventure.room_description())

    # load synonyms into main
    adventure.load_synonyms()

    # Prompt the user for commands until they type QUIT
    while True:

        # Prompt, converting all input to upper case
        command = input("> ").upper()

        # implement synonyms
        for key in adventure.synonyms:
            if command == key:
                command = adventure.synonyms.get(key)

        # if movement in right direction, move
        if adventure.conditional_move(command) or adventure.move(command):
            print(adventure.room_description())
            if adventure.item_present():
                for key in adventure.item():
                    print(adventure.item()[key])

            # conditional forced moves player back to adjacent room
            while adventure.forced_conditional_connection():
                adventure.conditional_move("FORCED")
                print(adventure.room_description())
                if adventure.item_present():
                    for key in adventure.item():
                        print(adventure.item()[key])

            # forced moves player back to adjacent room
            while adventure.forced_connection():
                adventure.move("FORCED")
                print(adventure.room_description())
                if adventure.item_present():
                    for key in adventure.item():
                        print(adventure.item()[key])

        # handles incorrect commands
        elif not adventure.move(command) and not adventure.conditional_move(command) and"TAKE" not in command and "DROP" not in command and command != "HELP" and command != "QUIT" and command != "INVENTORY" and command != "LOOK":
            print("Invalid command.")

        # execute taking of items
        if "TAKE" in command:
            commandlist = command.split(' ')
            string_item = commandlist[1]
            print(adventure.item_taken(string_item))

        # execute dropping of items
        if "DROP" in command:
            commandlist = command.split(' ')
            string_item = commandlist[1]
            print(adventure.item_dropped(string_item))

        # help statements
        if command == "HELP":
            print("You can move by typing directions such as EAST/WEST/IN/OUT")
            print("QUIT quits the game.")
            print("HELP prints instructions for the game.")
            print("LOOK lists the complete description of the room and its contents.")

        # execute look command
        if command == "LOOK":
            print(adventure.room_long_des())
            if adventure._current_room.has_item():
                for key in adventure.item():
                    print(adventure.item()[key])

        # execute inventory command
        if command == "INVENTORY":
            if adventure.inventory == {}:
                print("Your inventory is empty")
            else:
                for key in adventure.inventory:
                    print(adventure.inventory.get(key))

        # Allows player to exit the game loop
        if command == "QUIT":
            break
