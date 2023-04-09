''' Module depth_first.py
This module contains the Python implementation of depth first search applied to maze solving
Depth first search uses a stack.
It explores as far as possible along each branch before backtracking.
'''

##---------------------------Functions---------------------------##

def depth_first_search(graph: dict, start: tuple, goal: tuple) -> tuple[list, set, int]:
    '''
    Find path from start to end of the maze using depth first search

    :param graph: dictionary of adjacency lists generated from the input maze
    :param start: coordinates of the start node
    :param goal: coordinates of the goal node
    :returns path: list of coordinates representing path from start node to goal node
    :returns explored: list of coordinates representing nodes explored by the algorithm
    :return steps: number of steps to find the path
    '''

    # Depth first search uses a stack
    stack = [(start, [start])]
    explored = set()
    steps = 0

    while stack:
        (node, path) = stack.pop()
        steps += 1
        if node not in explored:
            if node == goal: # If goal node is reached
                return path, explored, steps
            explored.add(node)
            for neighbour in graph[node]: # Explore neighbouring nodes in order (below-right-left-top)
                stack.append((neighbour, path + [neighbour]))

    return path, explored, steps
