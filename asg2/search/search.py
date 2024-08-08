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



def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    current = problem.getStartState()

    nodes = util.Stack()  # initialize stack
    nodes.push(current)  # push initial node into stack

    visited = [current]  # list of expanded nodes
    parents = {current: (0, None)}  # dictionary of nodes and their parents

    while not nodes.isEmpty():  # executes until stack is empty
        current = nodes.pop()  # retrieves the element at the top of the stack
        if problem.isGoalState(current):  # late goal-check
            actions = []
            while parents[current][0] != 0:  # backtrack the current node to initial node(start)
                current, action = parents[current]
                actions.insert(0, action)
            return actions
        if current not in visited:  # add unvisited nodes to the visited list
            visited.append(current)
        for successor, action, cost in problem.getSuccessors(current):
            if successor not in visited:  # check for unvisited successor nodes
                nodes.push(successor)  # push all unvisited successor nodes to the stack
                parents[successor] = (current, action)  # save information for backtracking
    return []  # return empty list in the case of failure

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    current = problem.getStartState()

    nodes = util.Queue()  # initialize queue
    nodes.push(current)  # push initial node into queue

    expanded = [current]  # list of expanded nodes
    parents = {current: (0, None)}  # dictionary of nodes and their parents

    while not nodes.isEmpty():  # executes until queue is empty
        current = nodes.pop()  # retrieves the element at the front of the queue
        if problem.isGoalState(current):  # late goal-check
            actions = []
            while parents[current][0] != 0: # backtrack the current node to the initial node(start)
                current, action = parents[current]
                actions.insert(0, action)
            return actions
        for successor, action, cost in problem.getSuccessors(current):
            if successor not in expanded:  # check for unexpanded successor nodes
                expanded.append(successor)  # add nodes to the expanded list
                nodes.push(successor)  # push all unexpanded nodes to the queue
                parents[successor] = (current, action)  # save information for backtracking
    return []  # return empty list in the case of failure


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    current = (problem.getStartState(), 0)

    nodes = util.PriorityQueue()  # initialize priority queue
    nodes.push(current, 0)  # push initial node into queue

    expanded = {current[0] : 0}  # dictionary of expanded nodes and their total cost
    parents = {current[0]: (0, None)}  # dictionary of nodes and their parents

    while not nodes.isEmpty():  # keep going until queue is empty
        current = nodes.pop()  # retrieve the element with the lowest priority in the queue
        if problem.isGoalState(current[0]):  # late goal-check
            actions = []
            current = current[0]
            while parents[current][0] != 0:  # backtrack the current node to the initial node(start)
                current, action = parents[current]
                actions.insert(0, action)
            return actions
        for successor, action, cost in problem.getSuccessors(current[0]):  # get all successors
            totalCost = cost + current[1]  # calculate total cost to get to successor
            if successor not in expanded:  # check for unexpanded successor nodes
                parents[successor] = (current[0], action)  # save successors' parents and action for backtracking
                expanded[successor] = totalCost  # add nodes to expanded list
                nodes.push((successor, totalCost), totalCost)  # push nodes to the queue
            elif totalCost < expanded[successor]:  # do the same thing if successor has less cost than the expanded node
                parents[successor] = (current[0], action)
                expanded[successor] = totalCost
                nodes.push((successor, totalCost), totalCost)
    return []  # return empty list in the case of failure

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    current = (problem.getStartState(), 0)

    nodes = util.PriorityQueue()  # initialize priority queue
    nodes.push(current, 0)  # push initial node into queue

    expanded = {current[0]: 0}  # dictionary of expanded nodes and their total cost
    parents = {current[0]: (0, None)}  # dictionary of nodes and their parents

    while not nodes.isEmpty():  # keep going until queue is empty
        current = nodes.pop()  # retrieve the element with lowest priority in the queue
        if problem.isGoalState(current[0]):  # late goal-check
            actions = []
            current = current[0]
            while parents[current][0] != 0:  # backtrack the current node to the initial node(start)
                current, action = parents[current]
                actions.insert(0, action)
            return actions
        for successor, action, cost in problem.getSuccessors(current[0]):  # check for unexpanded successor nodes
            actualCost = cost + current[1]  # calculate actual cost to current successor node
            heuristicCost = heuristic(successor, problem)  # calculate heuristic cost to current successor node
            totalCost = actualCost + heuristicCost  # calculate total cost to current successor node
            if successor not in expanded:  # check for unexpanded nodes
                parents[successor] = current[0], action  # save successors' parents and action for backtracking
                expanded[successor] = totalCost  # add nodes to expanded list
                nodes.push((successor, actualCost), totalCost)  # push successor nodes to the queue
            elif totalCost < expanded[successor]:  # do the same thing if successor has less cost than the expanded node
                parents[successor] = current[0], action
                expanded[successor] = totalCost
                nodes.push((successor, actualCost), totalCost)
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
