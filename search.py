# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    current_state, path_actions, path_cost, visited_states = None, [], 0, {}
    fringe_list = util.Stack() # Stack to maintain the fringe list
    fringe_list.push((problem.getStartState(), [None], 0)) # Create a dummy successor for start node
    while not fringe_list.isEmpty(): # Continue to search until all nodes have been scanned
        current_state, path_actions, path_cost = fringe_list.pop() # Pop node from the fringe list
        visited_states[current_state] = True # Mark node as visited
        if problem.isGoalState(current_state):
            break # Break the loop if goal state is reached
        for state, action, cost in problem.getSuccessors(current_state): # For every child node
            if state in visited_states:
                continue # Skip the node if it is already visited
            else:
                # Add child node to fringe list; append previous actions to maintain the path
                fringe_list.push((state, path_actions + [action], cost))
    return path_actions[1:] # Skip the direction for the starting node added as dummy

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    current_state, path_actions, path_cost, visited_states = None, [], 0, {}
    fringe_list = util.Queue()  # Queue to maintain the fringe list
    fringe_list.push((problem.getStartState(), [None], 0))  # Create a dummy successor for start node
    while not fringe_list.isEmpty():  # Continue to search until all nodes have been scanned
        current_state, path_actions, path_cost = fringe_list.pop()  # Pop node from the fringe list
        visited_states[current_state] = True  # Mark node as visited
        if problem.isGoalState(current_state):
            break  # Break the loop if goal state is reached
        for state, action, cost in problem.getSuccessors(current_state):  # For every child node
            if state in visited_states:
                continue # Skip the node if it is already visited
            else:
                # Add child node to fringe list; append previous actions to maintain the path
                fringe_list.push((state, path_actions + [action], cost))
    return path_actions[1:]  # Skip the direction for the starting node added as dummy

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    current_state, path_actions, path_cost, visited_states = None, [], 0, {}
    fringe_list = util.PriorityQueue() # PriorityQueue to maintain the fringe list with cost as priority
    fringe_list.push((problem.getStartState(), [None], 0), 0)  # Create a dummy successor for start node
    while not fringe_list.isEmpty():  # Continue to search until all nodes have been scanned
        current_state, path_actions, path_cost = fringe_list.pop()  # Pop node from the fringe list
        visited_states[current_state] = True  # Mark node as visited
        if problem.isGoalState(current_state):
            break  # Break the loop if goal state is reached
        for state, action, cost in problem.getSuccessors(current_state):  # For every child node
            if state in visited_states:
                continue  # Skip the node if it is already visited
            else:
                # Update fringe list with child node as follows:
                # if child not in fringe list then add it with priority set as the total cost to reach the node
                # from start {g(n)}
                # else update the priority of the child node in fringe list with lower of existing path cost
                # and new path cost
                # prepend previous actions to maintain the path
                fringe_list.update((state, path_actions + [action], cost + path_cost), cost + path_cost)
    return path_actions[1:]  # Skip the direction for the starting node added as dummy

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    current_state, path_actions, path_cost, visited_states, explored_states = None, [], 0, set(), {}
    fringe_list = util.PriorityQueue()  # PriorityQueue to maintain the fringe list with cost as priority
    fringe_list.push((problem.getStartState(), [None], 0), 0)  # Create a dummy successor for start node
    while not fringe_list.isEmpty():  # Continue to search until all nodes have been scanned
        current_state, path_actions, path_cost = fringe_list.pop()  # Pop node from the fringe list
        explored_states[current_state] = True  # Mark node as visited
        if problem.isGoalState(current_state):
            break  # Break the loop if goal state is reached
        for state, action, cost in problem.getSuccessors(current_state):  # For every child node
            if state in visited_states or state in explored_states:
                continue  # Skip the node if it is already visited
            else:
                # Calculate priority as the sum of cost to reach the node n from start and the heuristic cost to reach
                # the goal state from the node n i.e. {f(n) = g(n) + h(n)}
                # Update fringe list with child node as follows:
                # if child not in fringe list then add it with priority
                # else update the priority of the child node in fringe list with lower of existing priority
                # and new priority
                # prepend previous actions to maintain the path
                g_of_n = path_cost + cost
                h_of_n = heuristic(state, problem)
                f_of_n = g_of_n + h_of_n
                visited_states.add(state)
                fringe_list.update((state, path_actions + [action], f_of_n), f_of_n)
    return path_actions[1:]  # Skip the direction for the starting node added as dummy

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
