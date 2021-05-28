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
import heapq

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
    initial_state =problem.getStartState()
    initial_node = [initial_state,[]]
    stack = util.Stack()
    visited = []
    stack.push(initial_node)
    while stack.isEmpty() == False:

        current_node = stack.pop()
        current = current_node[0]
        visited.append(current)
        if problem.isGoalState(current):
            return current_node[1]
        successors = problem.getSuccessors(current)

        for child in successors:
            used_for_append = (current_node[1]).copy()
            child_pt = child[0]
            used_for_append.append(child[1])
            if child_pt not in visited:
                child_node = [child_pt, used_for_append]
                stack.push(child_node)
    # util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    initial_state = problem.getStartState()
    initial_node = [initial_state, []]
    queue = util.Queue()
    visited = []
    queue.push(initial_node)
    while queue.isEmpty() == False:
        current_node = queue.pop()
        current = current_node[0]
        visited.append(current)
        if problem.isGoalState(current):
            return current_node[1]
        successors = problem.getSuccessors(current)
        for child in successors:
            used_for_append = (current_node[1]).copy()
            child_pt = child[0]
            used_for_append.append(child[1])
            not_in_queue = True
            for c in queue.list:
                if c[0] == child_pt:
                    not_in_queue = False
            if (child_pt not in visited) & not_in_queue:
                child_node = [child_pt, used_for_append]
                queue.push(child_node)
    #util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    # print(type(problem.getStartState()))
    "*** YOUR CODE HERE ***"
    initial_state = problem.getStartState()
    initial_node = [initial_state, [],0]
    piorityQueue = util.PriorityQueue()
    piorityQueue.push(initial_node,0)
    visited = []
    while piorityQueue.isEmpty() == False:
        current_node = piorityQueue.pop()
        current_vector = current_node[0]
        current_direction = current_node[1]
        current_cost = current_node[2]
        visited.append(current_vector)
        if problem.isGoalState(current_vector):
            return current_node[1]
        successors = problem.getSuccessors(current_vector)
        for child in successors:
            child_vector = child[0]
            new_path = current_direction.copy()
            new_path.append(child[1])
            new_cost = child[2] + current_cost
            next_node = (child_vector, new_path, new_cost)
            if (child_vector not in visited):
                for index, (p, c, i) in enumerate(piorityQueue.heap):
                    if i[0] == child_vector:
                        if p <= new_cost:
                            break
                        del piorityQueue.heap[index]
                        piorityQueue.heap.append((new_cost, c, next_node))
                        heapq.heapify(piorityQueue.heap)
                        break
                else:
                    piorityQueue.push(next_node, new_cost)

    #util.raiseNotDefined()

def nullHeuristic(state, problem=None ):#
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    #return util.manhattanDistance(problem.getStartState(),problem.goal)
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    initial_state = problem.getStartState()
    initial_node = [initial_state, [], 0]
    piorityQueue = util.PriorityQueue()
    piorityQueue.push(initial_node, heuristic(initial_state,problem))
    visited = []
    while piorityQueue.isEmpty() == False:
        current_node = piorityQueue.pop()

        current_vector = current_node[0]
        current_direction = current_node[1]
        current_cost = current_node[2]
        visited.append(current_vector)

        if problem.isGoalState(current_vector):
            return current_node[1]
        successors = problem.getSuccessors(current_vector)
        for next in successors:
            next_vector = next[0]
            next_path = current_direction.copy()
            next_path.append(next[1])
            next_cost = next[2] + current_cost
            next_priority = next_cost + heuristic(next_vector,problem)

            next_node = (next_vector, next_path, next_cost)
            if (next_vector not in visited):
                for index, (p, c, i) in enumerate(piorityQueue.heap):
                    if i[0] == next_vector:
                        if p <= next_priority:
                            break
                        del piorityQueue.heap[index]
                        piorityQueue.heap.append((next_priority, c, next_node))
                        heapq.heapify(piorityQueue.heap)
                        break
                else:
                    piorityQueue.push(next_node, next_priority)

    #util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
