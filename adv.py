from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()

'''
Understanding the problem...

Input:

Graph is undirected, cyclic, and connected

Nodes: rooms

Edges: baths between rooms

500 total nodes (rooms)

Output:

A traversal path that visits every room at least once and must be done in under 2000 moves

'''

'''
Ideas/Thoughts:

Will need to visit a room, find the possible exits, and then move one direction and do the same there and so on.

Will need to keep track of backtracking in the traversal path.

DFT will help me get as far as possible before needing to backtrack.
'''

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Use to find the opposite direction when backtracking
opposites = {"n": "s", "s": "n", "w": "e", "e": "w"}


# Basically this is a recursive depth first traversal that is also tracking the path including backtracking

def traverse_graph(current_room, visited=None):
    # holds the directions for traversing the graph
    directions = []

    # Creates the visited set on the first run through
    if visited == None:
        visited = set()

    # Get all exits for current room loop through them
    for direction in player.current_room.get_exits():
        # Travel selected direction
        player.travel(direction)

        # If we've been to this room, go back the opposite direction to go back to the original room
        if player.current_room in visited:
            player.travel(opposites[direction])

        # If we haven't been to this room
        else: 
            # Add room to visited
            visited.add(player.current_room)
            # Append the direction to our list of directions for the traversal
            directions.append(direction)
            # Using recursion repeat this process with your current room and add those directions to the path
            directions = directions + traverse_graph(player.current_room, visited)
            # Go back to the room before
            player.travel(opposites[direction])
            # Add the backtracking to the directions traversal
            directions.append(opposites[direction])
    # return the path that travels through all rooms
    return directions

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = traverse_graph(player.current_room)
print(traversal_path)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
