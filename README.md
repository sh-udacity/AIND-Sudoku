# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  

A: Prior to adding a naked twins constraint, our solver
would repeatedly apply the following two functions to
constrain what possible values still exist, removing
possible values from the state of board which violate the
rules of the game: `eliminate` to update all peers of a
solved box, removing the solved box's value from their list
of possible values, and `only_choice` to assign a value to a
box if its list of possible values contained a value which
no other box in its unit could use.

The idea of naked twins is that if two boxes in a unit share
the same two possible values, for example both are
represented with the value '37', we know no other box in
that unit may use '3' or '7'.

So I simply added a third function to process the state of
the board after `eliminate` and `only_choice`, called
`naked_twins`, which removes naked twins' values from each
peer's list of possible values, using a peer list scoped to
that specific unit.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  

A: Previously, the `eliminate` function would process each
box step by step, where if its value was a single digit, we
know no other peer can possibly use that value. Peer in this
context means a particular Sudoku grouping's boxes, one of
the vertical, horizontal, or square group that a given box
occurs in.

In order to cover the diagonal case, I simply added the two
new diagonal units to the expression that builds the
`unitlist`, which is then used when building every box's
list of peers. `eliminate` then does the rest, applying its
rule against the diagonal units as well when traversing the
state of the board.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

