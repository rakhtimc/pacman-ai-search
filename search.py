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
    visited_states = set() # Set to maintain visited nodes
    fringe_list = util.Stack() # Stack to maintain the fringe list
    fringe_list.push((problem.getStartState(), [], 0)) # Create a dummy successor for start node
    while not fringe_list.isEmpty(): # Continue to search until all nodes have been scanned
        current_state, path_actions, path_cost = fringe_list.pop()
        if problem.isGoalState(current_state):
            return path_actions # Return the path if goal is reached
        visited_states.add(current_state) # Add node to visited nodes
        for state, action, cost in problem.getSuccessors(current_state): # For every child node
            if state not in visited_states: # Skip if node is already visited
                # Add child node to fringe list; append previous actions to maintain the path
                fringe_list.push((state, path_actions + [action], cost))
    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    visited_states, explored_states = set(), set()  # Set to maintain visited and explored nodes
    fringe_list = util.Queue()  # Queue to maintain the fringe list
    visited_states.add(problem.getStartState())
    fringe_list.push((problem.getStartState(), [], 0))  # Create a dummy successor for start node
    while not fringe_list.isEmpty():  # Continue to search until all nodes have been scanned
        current_state, path_actions, path_cost = fringe_list.pop()
        if problem.isGoalState(current_state):
            return path_actions # Return the path if goal is reached
        explored_states.add(current_state) # Add node to explored nodes
        for state, action, cost in problem.getSuccessors(current_state):  # For every child node
            # Skip if node is already visited or explored
            if state not in visited_states and state not in explored_states:
                # Add child node to fringe list and visited nodes; append previous actions to maintain the path
                visited_states.add(state)
                fringe_list.push((state, path_actions + [action], cost))
    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    explored_states = set() # Set to maintain explored nodes
    fringe_list = util.PriorityQueue()  # PriorityQueue to maintain the fringe list
    fringe_list.push((problem.getStartState(), [], 0), 0)  # Create a dummy successor for start node
    while not fringe_list.isEmpty():  # Continue to search until all nodes have been scanned
        current_state, path_actions, path_cost = fringe_list.pop()
        if problem.isGoalState(current_state):
            return path_actions  # Return the path if goal is reached
        if current_state not in explored_states: # Explore current node only if not already explored
            explored_states.add(current_state) # Add node to explored nodes
            for state, action, cost in problem.getSuccessors(current_state):  # For every child node
                if state not in explored_states: # Skip if node is already explored
                    # Add child node to fringe list; append previous actions to maintain the path
                    # Calculate priority as cost to reach node n from start {f(n) = g(n)}
                    fringe_list.push((state, path_actions + [action], path_cost + cost), path_cost + cost)
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    explored_states = set()  # Set to maintain explored nodes
    fringe_list = util.PriorityQueue()  # PriorityQueue to maintain the fringe list
    fringe_list.push((problem.getStartState(), [], 0), 0)  # Create a dummy successor for start node
    while not fringe_list.isEmpty():  # Continue to search until all nodes have been scanned
        current_state, path_actions, path_cost = fringe_list.pop()
        if problem.isGoalState(current_state):
            return path_actions  # Return the path if goal is reached
        if current_state not in explored_states:  # Explore current node only if not already explored
            explored_states.add(current_state)  # Add node to explored nodes
            for state, action, cost in problem.getSuccessors(current_state):  # For every child node
                if state not in explored_states:  # Skip if node is already explored
                    # Add child node to fringe list; append previous actions to maintain the path
                    # Calculate priority as the sum of cost to reach the node n from start and the heuristic cost to
                    # reach the goal state from the node n i.e. {f(n) = g(n) + h(n)}
                    g_of_n = path_cost + cost
                    h_of_n = heuristic(state, problem)
                    f_of_n = g_of_n + h_of_n
                    fringe_list.push((state, path_actions + [action], g_of_n), f_of_n)
    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
