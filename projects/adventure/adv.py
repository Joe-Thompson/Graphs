from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
import os.path

map_file = "maps/main_maze.txt"
map_file = os.path.join(os.path.dirname(__file__), map_file)

# Read in all the words in one go

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
from collections import deque


def find_path(player, world):
    graph = {}
    path = []
    back_track_stack = deque()
    
    while len(graph) < len(world.rooms):
        current_room = player.current_room
        
        if current_room.id not in graph:
            add_room_to_graph(current_room, graph)
        unknown_direction = unexplored_directions(current_room, graph)
        
        if len(unknown_direction) > 0:
            new_direction = random.choice(unknown_direction)
            back_track_stack.append(opposite(new_direction))
            path.append(new_direction)
            player.travel(new_direction)
            next_room = player.current_room
            graph[current_room.id][new_direction] = next_room.id
            
            if next_room.id not in graph:
                add_room_to_graph(next_room, graph)
            graph[next_room.id][opposite(new_direction)] = current_room.id
            
        else:
            if len(back_track_stack) <= 0:
                return path
            
            back_track_path = back_track_stack.pop()
            path.append(back_track_path)
            player.travel(back_track_path)
            next_room = player.current_room
            graph[current_room.id][back_track_path] = next_room.id
            
    path.append(opposite(path[-1]))
    return path


def add_room_to_graph(room, graph):
    if room.id in graph:
        return
    exits = {}
    for exit_direction in room.get_exits():
        exits[exit_direction] = '?'
    graph[room.id] = exits


def opposite(direction):
    if direction == "n":
        return "s"
    elif direction == "s":
        return "n"
    elif direction == "e":
        return "w"
    elif direction == "w":
        return "e"
    else:
        return None


def unexplored_directions(room, graph):
    unknown_direction = []
    for (direction, roomID) in graph[room.id].items():
        if roomID == '?':
            unknown_direction.append(direction)
    return unknown_direction


traversal_path = find_path(player, world)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path[:-1]:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######e
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
