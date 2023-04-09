# Maze Solver README

## File Structure

The file containing answers is in the same folder as this README. It is called [answers.pdf](answers.pdf).

The main program file is the executable [main.py](main.py). It can be found in the initial folder, which also contains the source code for the algorithms implemented for the exercise, as well as the Graph class used by both of them:

+ Depth-first search: [depth_first.py](depth_first.py)
+ A* graph search: [a_star.py](a_star.py)
+ Graph class: [graph.py](graph.py)

Sample mazes provided with the specification and used for testing the algorithms can be found in the [/sample-mazes/](sample-mazes) folder. It also contains the [sample-results](/sample-mazes/sample-results) file used to store statistics obtained when running the algorithms on the sample mazes.

Statistics obtained when running the algorithms on a custom maze can be found in the same folder as the main script. The output file will be named after the name of the custom maze, with 'results' appended to the file name.

The [/extra-statistics](/extra-statistics) folder already contains statistics for weighted A* graph search (and depth-first) applied to the sample mazes. This is also the folder where statistics will be stored when running weighted A* for any maze (by entering 'h'). Note that when doing this, the output file will aslo contain statistics about depth-first search. This is done to allow the user to also experiment with different orderings of node expansion for depth-first.

## Running the program

The program is designed to be run from the command line. When in the terminal, make sure that you navigate to the folder containing the [main.py](main.py) file. This main script can then be executed by running:  
```python main.py```  

Please note that all the code was tested using Python 3.9, so it is recommended to use at this version to run the program. It is not guaranteed to run properly if using a previous version. If using multiple versions of Python on the same machine, one can run the program with a particular version using:  
```py -<version> main.py```  

When running [main.py](main.py), the user has four options to choose from:
+ Entering 's' will solve all sample mazes provided with the CA, and store the peformance statistics in [sample-results](/sample-mazes/sample-results)
+ Entering 'c' will allow the user to solve any maze, provided the input file is valid. The performance statistics will be stored in the same folder as the main script.
+ Entering 'h' will allow the user to experiment with different heuristics for A* for any maze, provided the input file is valid. The performance statistics will be stored in [/extra-statistics](/extra-statistics).
+ Entering 'q' will exit the program.


## Input File Validation

In order to be valid, an input file will need to be:
+ In the same folder as [main.py](main.py).
+ Of a similar format as sample mazes provided with the CA, with walls represented by '#' and paths by '-'.


## Notes

+ If the program cannot solve the maze, either because the input file cannot be found or the maze has no solution, the program will print the following to the console:  
```Error: file cannot be found or input is invalid```


