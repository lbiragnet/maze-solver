''' Module a_star.py
This module contains the Python implementation of A* graph search applied to maze solving
A* graph search uses a priority queue.
It stores the cost of a current path from the start node, and uses a heuristic function
to estimate the cost required to extend the path to the goal node.
'''

##---------------------------Imports---------------------------##

from queue import PriorityQueue

##---------------------------Heuristic Functions---------------------------##

def h(c1:tuple[int, int], c2:tuple[int, int]):
    '''
    Initial heuristic function used by A* graph search - estimates cost by calculating the
    Manhattan distance (distance measured along axes at right angles) between nodes
    
    :param c1: coordinates of the first node
    :param c2: coordinates of the second node
    :returns: the Manhattan distance between both nodes (sum of absolute differences)
    '''
    x1, y1 = c1[0], c1[1]
    x2, y2 = c2[0], c2[1]
    return abs(x1-x2) + abs(y1-y2)

def h0(c1:tuple[int, int], c2:tuple[int, int]):
    '''
    Heuristic function h(n) = 0 used for Dijkstra's algorithm
    
    :param c1: coordinates of the first node
    :param c2: coordinates of the second node
    :returns: 0
    '''
    return 0

def h_weighted(c1:tuple[int, int], c2:tuple[int, int]):
    '''
    Heuristic function used by weighted A* graph search - adds a weight to the
    Manhattan distance
    
    :param c1: coordinates of the first node
    :param c2: coordinates of the second node
    :returns: the weighted Manhattan distance between both nodes (sum of absolute differences)
    '''
    x1, y1 = c1[0], c1[1]
    x2, y2 = c2[0], c2[1]
    return 2.7*(abs(x1-x2) + abs(y1-y2))


##---------------------------Implementation of A*---------------------------##

def a_star_search(graph:dict, start:tuple, goal:tuple) -> tuple[list, list, int]:
    '''
    Find path from start to end of the maze using A* graph search

    :param graph: dictionary of adjacency lists generated from the input maze
    :param start: coordinates of the start node
    :param goal: coordinates of the goal node
    :returns final_path: list of coordinates representing path from start node to goal node
    :returns explored_list: list of coordinates representing nodes explored by the algorithm
    :returns steps: number of steps to find the path
    '''

    # A* graph search uses a priority queue
    q = PriorityQueue()
    g = {} # Store cost of current path
    f = {} # Store estimations of total costs (adding heuristic function)
    steps = 0

    # Initialise all costs to +infinity except for start node
    for i in graph.keys():
        g[i] = float('inf')
        f[i] = float('inf')
    g[start] = 0
    f[start] = h(start,(1,1))

    # Add start node and associated cost to the priority queue
    q.put((h(start,(1,1)),h(start,(1,1)),start))
    explored = {}

    # Main loop
    while not q.empty():
        node = q.get()[2] # Get node coordinates
        steps += 1
        # Break if goal node reached
        if node == goal:
            break
        # Store current and estimated cost of each neighbour
        for neighbour in graph[node]:
            g_calc = g[node] + 1
            f_calc = g_calc + h(neighbour, goal)
            # Choose node with lowest estimated cost
            if f_calc < f[neighbour]:
                g[neighbour] = g_calc
                f[neighbour] = f_calc
                q.put((f_calc, h(neighbour, goal), neighbour))
                explored[neighbour] = node # Add node to list of explored nodes

    # Backtracking from goal node to start node
    path = {}
    xy = goal
    while xy != start:
        steps += 1
        path[explored[xy]] = xy
        xy = explored[xy] # Go back through explored nodes until start node

    # Format path (listed in reverse order from backtracking)
    final_path = list(path.keys())
    final_path.reverse()
    final_path.append(goal)

    # Format list of explored nodes
    explored_list = list(explored.keys())
    explored_list.insert(0, start)

    return final_path, explored_list, steps



##---------------------------Further Heuristic Experimentation---------------------------##

def dijkstras(graph:dict, start:tuple, goal:tuple) -> tuple[list, list, int]:
    '''
    Same function as a_star_search except the heuristic is set to 0

    :param graph: dictionary of adjacency lists generated from the input maze
    :param start: coordinates of the start node
    :param goal: coordinates of the goal node
    :returns final_path: list of coordinates representing path from start node to goal node
    :returns explored_list: list of coordinates representing nodes explored by the algorithm
    :returns steps: number of steps to find the path
    '''
    q = PriorityQueue()
    g = {} # Store cost of current path
    f = {} # Store estimations of total costs (adding heuristic function)
    steps = 0

    # Initialise all costs to +infinity except for start node
    for i in graph.keys():
        g[i] = float('inf')
        f[i] = float('inf')
    g[start] = 0
    f[start] = h0(start,(1,1))

    # Add start node and associated cost to the priority queue
    q.put((h0(start,(1,1)),h0(start,(1,1)),start))
    explored = {}

    # Main loop
    while not q.empty():
        node = q.get()[2] # Get node coordinates
        steps += 1
        # Break if goal node reached
        if node == goal:
            break
        # Store current and estimated cost of each neighbour
        for neighbour in graph[node]:
            g_calc = g[node] + 1
            f_calc = g_calc + h0(neighbour, goal)
            # Choose node with lowest estimated cost
            if f_calc < f[neighbour]:
                g[neighbour] = g_calc
                f[neighbour] = f_calc
                q.put((f_calc, h0(neighbour, goal), neighbour))
                explored[neighbour] = node # Add node to list of explored nodes

    # Backtracking from goal node to start node
    path = {}
    xy = goal
    while xy != start:
        steps += 1
        path[explored[xy]] = xy
        xy = explored[xy] # Go back through explored nodes until start node

    # Format path (listed in reverse order from backtracking)
    final_path = list(path.keys())
    final_path.reverse()
    final_path.append(goal)

    # Format list of explored nodes
    explored_list = list(explored.keys())
    explored_list.insert(0, start)

    return final_path, explored_list, steps


def weighted_a_star(graph:dict, start:tuple, goal:tuple) -> tuple[list, list, int]:
    '''
    Weigthed version of the initial implementation of A* graph search

    :param graph: dictionary of adjacency lists generated from the input maze
    :param start: coordinates of the start node
    :param goal: coordinates of the goal node
    :returns final_path: list of coordinates representing path from start node to goal node
    :returns explored_list: list of coordinates representing nodes explored by the algorithm
    :returns steps: number of steps to find the path
    '''

    q = PriorityQueue()
    g = {} # Store cost of current path
    f = {} # Store estimations of total costs (adding heuristic function)
    steps = 0

    # Initialise all costs to +infinity except for start node
    for i in graph.keys():
        g[i] = float('inf')
        f[i] = float('inf')
    g[start] = 0
    f[start] = h_weighted(start,(1,1))

    # Add start node and associated cost to the priority queue
    q.put((h_weighted(start,(1,1)),h_weighted(start,(1,1)),start))
    explored = {}

    # Main loop
    while not q.empty():
        node = q.get()[2] # Get node coordinates
        steps += 1
        # Break if goal node reached
        if node == goal:
            break
        # Store current and estimated cost of each neighbour
        for neighbour in graph[node]:
            g_calc = g[node] + 1
            f_calc = g_calc + h_weighted(neighbour, goal)
            # Choose node with lowest estimated cost
            if f_calc < f[neighbour]:
                g[neighbour] = g_calc
                f[neighbour] = f_calc
                q.put((f_calc, h_weighted(neighbour, goal), neighbour))
                explored[neighbour] = node # Add node to list of explored nodes

    # Backtracking from goal node to start node
    path = {}
    xy = goal
    while xy != start:
        steps += 1
        path[explored[xy]] = xy
        xy = explored[xy] # Go back through explored nodes until start node

    # Format path (listed in reverse order from backtracking)
    final_path = list(path.keys())
    final_path.reverse()
    final_path.append(goal)

    # Format list of explored nodes
    explored_list = list(explored.keys())
    explored_list.insert(0, start)

    return final_path, explored_list, steps
