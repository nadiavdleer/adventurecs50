# loader.py
#
# Minor programmeren
# Nadia van der Leer
#
# - file to load all rooms, items and connections into dictionaries and classes

from room import Room
from item import Item


def load_room_graph(filename):
    # initialise rooms dictionary, set count to 1
    rooms = {}
    count = 1

    with open(filename) as f:
        # Load Rooms into rooms dictionary
        while True:
            line = f.readline()
            if line == "\n":
                break
            line = line.rstrip()
            line_list = line.split("\t")
            room = Room(line_list[0], line_list[1], line_list[2])
            rooms[count] = room
            count += 1

        # Load (conditional) connections and add them to rooms
        while True:
            line = f.readline()
            if line == "\n":
                break
            line = line.rstrip()
            line_list = line.split("\t")
            source_room = int(line_list[0])

            for i in (range(1, len(line_list) - 1, 2)):
                if len(line_list[i+1]) > 2:

                    conditional_list = line_list[i+1].split("/")
                    conditional_room = int(conditional_list[0])
                    conditional_item = conditional_list[1]

                    destination_room = rooms[conditional_room]

                    rooms[source_room].add_conditional_connection(line_list[i], destination_room)

                    rooms[source_room].items_needed[destination_room] = conditional_item

                else:
                    rooms[source_room].add_connection(line_list[i], rooms[int(line_list[i+1])])

        # load items into rooms
        while True:
            line = f.readline()
            if line == "":
                break
            line = line.rstrip()
            line_list = line.split("\t")

            item_room = rooms[int(line_list[2])]
            item_name = line_list[0]
            item_description = line_list[1]
            item = Item(item_name, item_description, item_room)

            item_room.dict_items[item_name] = item

    # make sure default setting is first room
    return rooms[1]

