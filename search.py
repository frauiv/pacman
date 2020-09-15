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

def search_dfs(problem, object):
    discovered = []
    object.push([0,(problem.getStartState(), 'Stop', 0)])
    possible_states = []
    list_of_actions = []
    # We will use queue and a list
    while (not object.isEmpty()):
        state = object.pop()
    
        state_location = state[1][0]
        
        moveNum = state[0]
        if problem.isGoalState(state_location):
            # print list_of_actions
            # just the actions
            possible_states.append((moveNum, state[1][1]))
            for x in possible_states:
                if(x[1] != 'Stop'):
                    list_of_actions.append(x[1])
            return list_of_actions
        
        
        if state_location not in discovered:
            discovered.append(state_location)

            #only do this move after start state has been popped 
            if state[1][1] != 'Stop':
               # print moveNum
                if moveNum <= possible_states[-1][0]:
                #want copy from start of list to predessor 
                    possible_states = possible_states[0:moveNum]

            #only append move number and action 
            possible_states.append((moveNum, state[1][1]))
            for successor in problem.getSuccessors(state_location):
                if successor[0] not in discovered:
                    object.push([moveNum+1, successor])
    return []

def search_bfs(problem, object):
    discovered = []
    object.push([-1,(problem.getStartState(), "Stop", 0)])
    possible_states = []
    list_of_actions =[]
    # We will use queue and a list
    while (not object.isEmpty()):
        state = object.pop()
        #get the current state location and parent location in list
        state_location = state[1][0]
        parent_list_index = state[0]

        if problem.isGoalState(state_location):
            # print list_of_actions
            # just the action
            possible_states.append((parent_list_index, state[1][1]))
            list_of_actions.append(state[1][1])
            while(parent_list_index != 0):
                state_to_add = possible_states[parent_list_index]
                list_of_actions.append(state_to_add[1])
                parent_list_index = state_to_add[0]
            list_of_actions.reverse()
            
            return list_of_actions

        #only will add successors and append to list if current location not discovered 
        if state_location not in discovered:
            #add current satate to discovered list
            discovered.append(state_location)
            
            #append parents location in possible state list 
            #alpng with the action state and state location on board 
            possible_states.append((parent_list_index, state[1][1]))

            #get location of parent in the possible states list 
            parent_list_index = len(possible_states)-1

            #get successors and add them to queue 
            for successor in problem.getSuccessors(state_location):
                if successor[0] not in discovered:
                    #only append parent location in possible states and the successor 
                    object.push([parent_list_index,successor])
    return []

def search_ucs(problem, object):
    discovered = []
    object.push([-1,0,(problem.getStartState(), "Stop", 0)],2)
    possible_states = []
    list_of_actions =[]
    
    # We will use queue and a list
    while (not object.isEmpty()):
        state = object.pop()
        #get the current state location, parent location in list, and total running cost
        state_location = state[2][0]
        parent_list_index = state[0]
        #current_cost = state[0][1][2]+state[1]
        #print state

        if problem.isGoalState(state_location):
            # print list_of_actions
            # just the action
            possible_states.append((parent_list_index, state[2][1][1]))
            
            list_of_actions.append(state[2][1])
            while(parent_list_index != 0):
                state_to_add = possible_states[parent_list_index]
                list_of_actions.append(state_to_add[1])
                parent_list_index = state_to_add[0]
            list_of_actions.reverse()

            return list_of_actions

        #only will add successors and append to list if current location not discovered 
        if state_location not in discovered:
            #add current satate to discovered list
            discovered.append(state_location)
            
            #append parents location in possible state list 
            #along with the action state and state location on board 
            possible_states.append((parent_list_index, state[2][1], state[1]))

            #get location of parent in the possible states list 
            parent_list_index = len(possible_states)-1

            #get successors and add them to queue 
            for successor in problem.getSuccessors(state_location):
                if successor[0] not in discovered:
                    #only append parent location in possible states and the successor 
                    object.push([parent_list_index, state[1]+successor[2],successor],state[1]+successor[2])
                else:
                    #if the successor is discovered, check if it needs to be updated
                    new_path_cost = state[1]+successor[2]
                    object.update2(state, new_path_cost,successor)
                    
    return []

def depthFirstSearch(problem):
    # Initialize an empty Stack
    object = util.Stack()
    # DFS is general graph search with a Stack as the data structure
    return search_dfs(problem, object)
    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    object = util.Queue()
    return search_bfs(problem, object)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    object = util.PriorityQueue()
    # DFS is general graph search with a Stack as the data structure
    return search_ucs(problem, object)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
