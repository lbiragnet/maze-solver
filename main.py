''' Module main.py
This module contains utility functions to parse input from a maze file.
It contains an executable function main() which runs the program.
'''

##---------------------------Imports---------------------------##

from timeit import default_timer as timer
from graph import Graph
from depth_first import depth_first_search
from a_star import a_star_search, dijkstras, weighted_a_star


##---------------------------Utility functions---------------------------##

def parse_input(filename:str) -> list[str]:
    '''
    Parse the input of a file to create a maze

    :param filename: text file containing the characters "#" and "-" forming a maze
    :returns: a 2D array representing a maze
    '''

    maze = []

    with open(filename, encoding="utf-8") as file: # Open the input file
        for inputLine in file:
            line = inputLine.rstrip() # Remove extra whitespaces
            chars = line.split(" ")
            if chars != [""]: # Remove extra lines
                maze.append(chars)

    return maze


def parse_graph(maze:list[str]) -> Graph:
    '''
    Create a Graph instance from the parsed input

    :param maze: a 2D array as returned by parse_input()
    :returns: the newly created Graph instance
    '''

    g = Graph()

    # Construct the adjacency list of each node
    for x in range(len(maze)):
        for y in range(1, len(maze[0])):
            if maze[x][y] != '#':
                nodes = []

                # Order of neighbouring nodes expansion - can be modified using comments
                
                # INITIAL ORDER: bottom - right - left - top
                if x > 0 and maze[x - 1][y] != '#': # Top node
                    nodes.append((x - 1, y))
                if y > 0 and maze[x][y - 1] != '#': # Left node
                    nodes.append((x, y - 1))
                if y < (len(maze[0]) - 1) and maze[x][y + 1] != '#': # Right node
                    nodes.append((x, y + 1))
                if x < (len(maze) - 1) and maze[x + 1][y] != '#': # Bottom node
                    nodes.append((x + 1, y))
                
                '''    
                # ORDER: right - bottom - left - top
                if x > 0 and maze[x - 1][y] != '#': # Top node
                    nodes.append((x - 1, y))
                if y > 0 and maze[x][y - 1] != '#': # Left node
                    nodes.append((x, y - 1))
                if x < (len(maze) - 1) and maze[x + 1][y] != '#': # Bottom node
                    nodes.append((x + 1, y))
                if y < (len(maze[0]) - 1) and maze[x][y + 1] != '#': # Right node
                    nodes.append((x, y + 1))
                    
                # ORDER: left - bottom - right - top
                if x > 0 and maze[x - 1][y] != '#': # Top node
                    nodes.append((x - 1, y))
                if y < (len(maze[0]) - 1) and maze[x][y + 1] != '#': # Right node
                    nodes.append((x, y + 1))
                if x < (len(maze) - 1) and maze[x + 1][y] != '#': # Bottom node
                    nodes.append((x + 1, y))
                if y > 0 and maze[x][y - 1] != '#': # Left node
                    nodes.append((x, y - 1))
                
                # ORDER: left - right - bottom - top
                if x > 0 and maze[x - 1][y] != '#': # Top node
                    nodes.append((x - 1, y))
                if x < (len(maze) - 1) and maze[x + 1][y] != '#': # Bottom node
                    nodes.append((x + 1, y))
                if y < (len(maze[0]) - 1) and maze[x][y + 1] != '#': # Right node
                    nodes.append((x, y + 1))
                if y > 0 and maze[x][y - 1] != '#': # Left node
                    nodes.append((x, y - 1))
                '''
                
                # Store the adjacency list of each node
                g.adjacency[(x, y)] = nodes

    return g


def calc_goal(maze:list[str]) -> tuple:
    '''
    Find the coordinates of the goal node in the maze, i.e., the coordinates to reach

    :param maze: a 2D array as returned by parse_input()
    :returns (x, y): the coordinates of the goal node in the maze
    '''

    y = -1
    x = len(maze) - 1 # Goal node is at the bottom of the maze
    # Iterate through the last line of the maze to find a path node (-)
    for i in range(0, len(maze[-1])):
        if maze[-1][i] == "-":
            y = i
            break
    if y == -1:
        return "No valid goal was found" # Return if no path node (-) found on last line
    return (x, y)


def setup_operations(input_f:str) -> tuple[Graph, tuple, tuple]:
    '''
    Parse the maze from the input file to create a graph and find the goal node

    :param input_f: the name of the input file (e.g., 'maze-Example.txt')
    :returns parsed_graph: the Graph instance parsed from the input file
    :returns start_node: the coordinates of the start node
    :returns goal_node: the coordinates of the goal node
    '''

    parsed_input = parse_input(input_f) # Create the 2D array of the maze
    parsed_graph = parse_graph(parsed_input) # Create the Graph instance
    start_node = (0, 1) # Start node is assumed to be at (0,1)
    return parsed_input, parsed_graph, start_node


def format_output_string(algorithm:str, maze_name:str, maze_path:list, maze_explored:list, maze_steps:int, exec_time:float) -> str:
    '''
    Format the results to output a single string

    :param algorithm: the name of the algorithm used
    :param maze_name: the name of the maze
    :param maze_path: the path found
    :param maze_explored: the list of explored nodes
    :param maze_steps: the number of steps taken
    :param exec_time: the execution time
    :returns output_str: the output string
    '''

    output_str = "RESULTS FOR " + maze_name + " USING " + algorithm + ":\n"
    output_str += ("Path found: " + str(maze_path) + "\n")
    output_str += ("Path length: " + str(len(maze_path)) + "\n")
    output_str += ("Number of explored nodes: " + str(len(list(maze_explored))) + "\n")
    output_str += ("Number of steps: " + str(maze_steps) + "\n")
    output_str += ("Execution Time: " + str(exec_time) + " seconds\n\n\n")

    return output_str


def solve_sample_mazes() -> str:
    '''
    This function runs the depth first and A* search algorithms for all mazes provided in the specification
    It formats statistics and outputs them to a file called "sample-results.txt"
    
    :returns: the name of the output file
    '''

    ##---------------------------Parsing and setup operations---------------------------##

    # Parse input file and create graph from maze
    input_easy = "sample-mazes/maze-Easy.txt"
    input_medium = "sample-mazes/maze-Medium.txt"
    input_large = "sample-mazes/maze-Large.txt"
    input_vlarge = "sample-mazes/maze-VLarge.txt"

    # Parse the graphs and find the start and goal nodes for each maze
    parsed_easy, graph_easy, start_easy= setup_operations(input_easy)
    parsed_medium, graph_medium, start_medium= setup_operations(input_medium)
    parsed_large, graph_large, start_large= setup_operations(input_large)
    parsed_vlarge, graph_vlarge, start_vlarge= setup_operations(input_vlarge)

    ##---------------------------Solve mazes using depth first search---------------------------##

    # Solve easy maze
    timestamp_easy_1_dfs = timer()
    goal_easy = calc_goal(parsed_easy) # Find the goal node
    path_easy_dfs, explored_easy_dfs, steps_easy_dfs = depth_first_search(graph_easy.adjacency, start_easy, goal_easy)
    timestamp_easy_2_dfs = timer()
    time_easy_dfs = timestamp_easy_2_dfs - timestamp_easy_1_dfs

    # Solve medium maze
    timestamp_medium_1_dfs = timer()
    goal_medium = calc_goal(parsed_medium) # Find the goal node
    path_medium_dfs, explored_medium_dfs, steps_medium_dfs = depth_first_search(graph_medium.adjacency, start_medium, goal_medium)
    timestamp_medium_2_dfs = timer()
    time_medium_dfs = timestamp_medium_2_dfs - timestamp_medium_1_dfs

    # Solve large maze
    timestamp_large_1_dfs = timer()
    goal_large = calc_goal(parsed_large) # Find the goal node
    path_large_dfs, explored_large_dfs, steps_large_dfs = depth_first_search(graph_large.adjacency, start_large, goal_large)
    timestamp_large_2_dfs = timer()
    time_large_dfs = timestamp_large_2_dfs - timestamp_large_1_dfs

    # Solve very large maze
    timestamp_vlarge_1_dfs = timer()
    goal_vlarge = calc_goal(parsed_vlarge) # Find the goal node
    path_vlarge_dfs, explored_vlarge_dfs, steps_vlarge_dfs = depth_first_search(graph_vlarge.adjacency, start_vlarge, goal_vlarge)
    timestamp_vlarge_2_dfs = timer()
    time_vlarge_dfs = timestamp_vlarge_2_dfs - timestamp_vlarge_1_dfs

    ##---------------------------Solve mazes using A* graph search---------------------------##

    # Solve easy maze
    timestamp_easy_1_astar = timer()
    goal_easy = calc_goal(parsed_easy) # Find the goal node
    path_easy_astar, explored_easy_astar, steps_easy_astar = a_star_search(graph_easy.adjacency, start_easy, goal_easy)
    timestamp_easy_2_astar = timer()
    time_easy_astar = timestamp_easy_2_astar - timestamp_easy_1_astar

    # Solve medium maze
    timestamp_medium_1_astar = timer()
    goal_medium = calc_goal(parsed_medium) # Find the goal node
    path_medium_astar, explored_medium_astar, steps_medium_astar = a_star_search(graph_medium.adjacency, start_medium, goal_medium)
    timestamp_medium_2_astar = timer()
    time_medium_astar = timestamp_medium_2_astar - timestamp_medium_1_astar

    # Solve large maze
    timestamp_large_1_astar = timer()
    goal_large = calc_goal(parsed_large) # Find the goal node
    path_large_astar, explored_large_astar, steps_large_astar = a_star_search(graph_large.adjacency, start_large, goal_large)
    timestamp_large_2_astar = timer()
    time_large_astar = timestamp_large_2_astar - timestamp_large_1_astar

    # Solve very large maze
    timestamp_vlarge_1_astar = timer()
    goal_vlarge = calc_goal(parsed_vlarge) # Find the goal node
    path_vlarge_astar, explored_vlarge_astar, steps_vlarge_astar = a_star_search(graph_vlarge.adjacency, start_vlarge, goal_vlarge)
    timestamp_vlarge_2_astar = timer()
    time_vlarge_astar = timestamp_vlarge_2_astar - timestamp_vlarge_1_astar

    ##---------------------------Output to file---------------------------##

    # Create/open the output file to overwrite it
    f = open("sample-mazes/sample-results.txt", "w")

    # Format output for depth first search
    output_str_easy_dfs = format_output_string("DEPTH FIRST SEARCH", "maze-Easy", path_easy_dfs, explored_easy_dfs, steps_easy_dfs, time_easy_dfs)
    output_str_medium_dfs = format_output_string("DEPTH FIRST SEARCH", "maze-Medium", path_medium_dfs, explored_medium_dfs, steps_medium_dfs, time_medium_dfs)
    output_str_large_dfs = format_output_string("DEPTH FIRST SEARCH", "maze-Large", path_large_dfs, explored_large_dfs, steps_large_dfs, time_large_dfs)
    output_str_vlarge_dfs = format_output_string("DEPTH FIRST SEARCH", "maze-VLarge", path_vlarge_dfs, explored_vlarge_dfs, steps_vlarge_dfs, time_vlarge_dfs)
    output_list_dfs = [output_str_easy_dfs, output_str_medium_dfs, output_str_large_dfs, output_str_vlarge_dfs]

    # Format output for A* graph search
    output_str_easy_astar = format_output_string("A* GRAPH SEARCH", "maze-Easy", path_easy_astar, explored_easy_astar, steps_easy_astar, time_easy_astar)
    output_str_medium_astar = format_output_string("A* GRAPH SEARCH", "maze-Medium", path_medium_astar, explored_medium_astar, steps_medium_astar, time_medium_astar)
    output_str_large_astar = format_output_string("A* GRAPH SEARCH", "maze-Large", path_large_astar, explored_large_astar, steps_large_astar, time_large_astar)
    output_str_vlarge_astar = format_output_string("A* GRAPH SEARCH", "maze-VLarge", path_vlarge_astar, explored_vlarge_astar, steps_vlarge_astar, time_vlarge_astar)
    output_list_astar = [output_str_easy_astar, output_str_medium_astar, output_str_large_astar, output_str_vlarge_astar]

    # Write to output file
    f.write("------------------------------DEPTH FIRST SEARCH RESULTS------------------------------\n\n")
    for line in output_list_dfs:
        f.write(line)
    f.write("-------------------------------A* GRAPH SEARCH RESULTS-------------------------------\n\n")
    for line in output_list_astar:
        f.write(line)
    f.close()

    return "sample-results.txt"


def solve_custom_maze(input_f:str) -> str:
    '''
    This function runs the depth first and A* search algorithms for a maze given by the user
    It formats statistics and outputs them to a file called "<filename>-results.txt"
    
    :param input_f: the name of the input file
    :returns: the name of the output file
    '''

    ##---------------------------Parsing and setup operations---------------------------##

    # Parse the input file, construct maze graph and find the start and goal nodes for each maze
    parsed, graph, start = setup_operations(input_f)

    ##---------------------------Solve maze using depth first search---------------------------##

    # Solve custom maze
    timestamp_1_dfs = timer()
    goal = calc_goal(parsed) # Find the goal node
    path_dfs, explored_dfs, steps_dfs = depth_first_search(graph.adjacency, start, goal)
    timestamp_2_dfs = timer()
    time_dfs = timestamp_2_dfs - timestamp_1_dfs

    ##---------------------------Solve maze using A* graph search---------------------------##
    
    # Solve custom maze
    timestamp_1_astar = timer()
    goal = calc_goal(parsed) # Find the goal node
    path_astar, explored_astar, steps_astar = a_star_search(graph.adjacency, start, goal)
    timestamp_2_astar = timer()
    time_astar = timestamp_2_astar - timestamp_1_astar

    ##---------------------------Output to file---------------------------##

    # Create/open the output file
    custom_name = input_f.split('.')[0]
    results_filename = custom_name + "-results.txt"
    f = open(results_filename, "w")

    # Format output for depth first search
    output_str_dfs = format_output_string("DEPTH FIRST SEARCH", custom_name, path_dfs, explored_dfs, steps_dfs, time_dfs)

    # Format output for A* graph search
    output_str_astar = format_output_string("A* GRAPH SEARCH", custom_name, path_astar, explored_astar, steps_astar, time_astar)

    # Write to output file
    f.write("------------------------------DEPTH FIRST SEARCH RESULTS------------------------------\n\n")
    f.write(output_str_dfs)
    f.write("-------------------------------A* GRAPH SEARCH RESULTS-------------------------------\n\n")
    f.write(output_str_astar)
    f.close()

    return results_filename


def test_heuristics(input_f:str) -> str:
    '''
    This function allows the user to experiment with different heuristics for A* and neighbour nodes expansion orders
    for depth first, on a maze given by the user
    It formats statistics and outputs them to a file called "<filename>-heuristics.txt"
    
    :param input_f: the name of the input file
    :returns: the name of the output file
    '''
    ##---------------------------Parsing and setup operations---------------------------##

    # Parse the input file, construct maze graph and find the start and goal nodes for each maze
    parsed, graph, start = setup_operations(input_f)

    ##---------------------------Solve maze using weighted A*---------------------------##

    # Solve custom maze
    timestamp_1_wastar = timer()
    goal = calc_goal(parsed) # Find the goal node
    path_wastar, explored_wastar, steps_wastar = weighted_a_star(graph.adjacency, start, goal)
    timestamp_2_wastar = timer()
    time_wastar = timestamp_2_wastar - timestamp_1_wastar

    ##---------------------------Output to file---------------------------##

    # Create/open the output file
    custom_name = input_f.split('.')[0]
    results_filename = custom_name + "-heuristics.txt"
    results_file_path = "extra-statistics/" + results_filename
    f = open(results_file_path, "w")

    # Format output for A* graph search
    output_str_wastar = format_output_string("WEIGHTED A* GRAPH SEARCH", custom_name, path_wastar, explored_wastar, steps_wastar, time_wastar)

    # Write to output file
    f.write("-------------------------------WEIGHTED A* RESULTS-------------------------------\n\n")
    f.write(output_str_wastar)
    f.close()

    return results_filename




##-------------------------------MAIN PROGRAM LOOP-------------------------------##

if __name__ == '__main__':

    # Welcome message
    print("Welcome to the Maze Solver! This program uses depth first search and a* graph search to solve mazes\n")
    
    menu_str = "Enter 's' if you would like to solve the provided sample mazes using both algorithms.\n"
    menu_str += "Enter 'c' if you would like to solve a custom maze.\n"
    menu_str += "Enter 'h' if you would like to experiment with different heuristics.\n"
    menu_str += "Enter 'q' to exit the program. \n"

    user_input = ""

    # Don't exit the program until the user enters 'q'
    while user_input not in ["q", "Q"]:
        user_input = input(menu_str)

        # Solve sample mazes
        if user_input in ["s", "S"]:
            print("Solving the sample mazes...\n")
            solve_sample_mazes()
            print("Mazes solved! Results can be found in the 'sample-results.txt' file.\n")

        # Solve custom maze
        elif user_input in ["c", "C"]:
            print("\nMake sure that the maze file is a .txt file within the same folder as the main script")
            print("The file must contain lines of the characters '#' (wall) or '-' (path) representing a maze.\n")
            input_file = input("Please enter the name of the file (e.g.: 'examplefile.txt'): ")
            # Check that filename is valid
            if not input_file.endswith(".txt"):
                print("\nFilename is invalid\n")
            else:
                #try:
                print("\nSolving the custom maze...")
                custom_results = solve_custom_maze(input_file)
                print("Maze solved! Results can be found in the "+ custom_results + " file.\n")
                #except:
                    #print("\nError: file cannot be found or input is invalid\n")
        elif user_input in ["h", "H"]:
            print("\nMake sure that the maze file is a .txt file within the same folder as the main script")
            print("The file must contain lines of the characters '#' (wall) or '-' (path) representing a maze.\n")
            input_file = input("Please enter the name of the file (e.g.: 'examplefile.txt'): ")
            # Check that filename is valid
            if not input_file.endswith(".txt"):
                print("\nFilename is invalid\n")
            else:
                try:
                    print("\nSolving the maze using different heuristics...")
                    custom_results = test_heuristics(input_file)
                    print("Maze solved! Results can be found in the "+ custom_results + " file.\n")
                except:
                    print("\nError: file cannot be found or input is invalid\n")