import os
import sys
import random
import time
import copy
import argparse


class State:
    def __init__(self, name, neighbors):
        self.name = name
        self.neighbors = neighbors
        self.color = ''
        self.colored = False


# ---------------GLOBAL VARS---------------
colors = []
states = []
pairings = []
graph = {}
domains = []
queue = []
neighbors_list = []
steps = 0

# We use this parser to read in input, in this case a file, in command lind in command
# ---------------PARSER---------------
parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()
with open(args.filename) as f:
#with open(os.path.join(sys.path[0], "usTestFile"), "r") as f:
    # split input into the 3 sections
    sections = f.read().split("\n\n")
    # step 1: create a list of colors, states, and domains
    colors = sections[0].split()
    states = sections[1].split()
    for state in states:
        domains.append(colors)
    # step 2: update graph dict with state keys
    for state in states:
        graph.update({state:[]})
    # step 3: update state keys with paired neighbor values
    for pair in sections[2].split("\n"):
        neighbor = pair.strip()
        pairings.append(neighbor)
        for key in graph.keys():
            if key in neighbor.split():
                for new_connected in neighbor.split():
                    if new_connected != key:
                        graph[key].append(new_connected)
# step 4: clear old list of states and fill w/ State class nodes
states.clear()
state_strings = []
for key, value in graph.items():
    states.append(State(key, value))
    state_strings.append(key)
    neighbors_list.append(value)
# step 5: start coloring nodes
colored_states = 0
steps = 0


# -----Local Search, Hill Climbing-----

#Main function: calls Hill_Climbing and starts timer
def main():
    Hill_Climbing()
    tic = time.perf_counter()


def Hill_Climbing():
    global total_conflicts #Total numbers of neiboring states with same color
    global iterations
    global steps

    iterations = 0
    steps = 0
    # randomly assign colors to states
    for state in states:
        state.color = random.choice(colors)
    # calculate initial total conflicts through heuristic_cost function
    total_conflicts = heuristic_cost(states);
    print("Initial conflicts: " + str(total_conflicts))
    # keep looping till total_conflicts is zero or no solution found
    while total_conflicts > 0:
        iterations = iterations + 1
        great_to_least(states) #check conflicts for each state
        if time.perf_counter() >= 60:
            print("No solution found.")
            #print(str(total_conflicts)) # maybe put in
            #for state in states:
            #    if state.conflicts > 0:
            #        print(state.name)
            sys.exit()
    print("Final conflicts: " + str(total_conflicts))
    print("Number of iterations: "+str(iterations))
    print("Time:" + str(time.perf_counter()))
    print("States recolored: " + str(steps))
    #print("Double check final conflicts: " + str(heuristic_cost(states)))
    for state in states:
        print(state.name+":"+state.color)

# find the actual object
def find_object(name):
    for state in states:
        if state.name == name:
            return state

# calculating the cost for each state and total
def heuristic_cost(states):
    conflicts = 0
    for state in states:
        state.conflicts = 0
        for neighbor in state.neighbors:
            neighbor_object = find_object(neighbor)
            if state.color == neighbor_object.color:
                state.conflicts = state.conflicts + 1
                conflicts = conflicts + 1
    return conflicts


def great_to_least(states):
    global total_conflicts
    global steps
    for state in states:
        if state.conflicts >= 3:
            successor_function(state) #check to change color, but check ones that have more conflicts
    for state in states:
        if state.conflicts > 0:
            successor_function(state)


def successor_function(state):
    global total_conflicts
    global steps
    for neighbor in state.neighbors:
                neighbor_object = find_object(neighbor)
                if state.color == neighbor_object.color:
                    oldColor = neighbor_object.color # keep color of neighbor
                    newColor = random.choice(colors) #assign another random color to neighbor
                    if newColor == oldColor:
                        newColor = random.choice(colors)
                    neighbor_object.color = newColor
                    new_conflicts = heuristic_cost(states)
                    if new_conflicts > total_conflicts:
                        total_conflicts = total_conflicts
                        neighbor_object.color = oldColor
                    else:
                        total_conflicts = new_conflicts
                        neighbor_object.color = newColor
                        steps = steps + 1



if __name__== "__main__":
  main()
