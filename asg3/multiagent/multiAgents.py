# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        score = 0
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        if newScaredTimes[0] <= 2:
            for ghostState in newGhostStates:
                ghostPosition = ghostState.getPosition()
                score += manhattanDistance(ghostPosition, newPos)
                if manhattanDistance(ghostPosition, newPos) < 2:
                    score -= 100

        newFood = successorGameState.getFood()
        oldFood = currentGameState.getFood()
        foodDistance = [manhattanDistance(newPos, food) for food in newFood.asList()]
        if len(foodDistance) != 0:
            minFoodDistance = min(foodDistance)
            score -= 1.5 * minFoodDistance
        if len(oldFood.asList()) > len(newFood.asList()):
            score += 50
        # print(action, score, minFoodDistance)
        return score

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def minimax(state, depth, agentIndex):
            if depth == 0 or state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            successorStates = []
            for legalAction in state.getLegalActions(agentIndex):
                successorStates.append(state.generateSuccessor(agentIndex, legalAction))
            if agentIndex == 0:
                scores = [minimax(successorState, depth, agentIndex+1) for successorState in successorStates]
                return max(scores)
            else:
                if agentIndex == state.getNumAgents() - 1:
                    depth -= 1
                    agentIndex = 0
                else:
                    agentIndex += 1
                scores = [minimax(successorState, depth, agentIndex) for successorState in successorStates]
                return min(scores)

        state = {}

        for action in gameState.getLegalActions(0):
            state[action] = minimax(gameState.generateSuccessor(0, action), self.depth, 1)

        bestAction = None
        highest = float('-inf')
        for action, score in state.items():
            if score > highest:
                highest = score
                bestAction = action

        return bestAction






        util.raiseNotDefined()


import math


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """

        def minimax(state, depth, agentIndex, alpha, beta):
            if depth == 0 or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            if agentIndex == 0:
                max = float('-inf')
                for legalAction in state.getLegalActions(agentIndex):
                    successorState = state.generateSuccessor(agentIndex, legalAction)
                    successorScore = minimax(successorState, depth, agentIndex + 1, alpha, beta)
                    if successorScore > max:
                        max = successorScore
                    if successorScore > alpha:
                        alpha = successorScore
                        if alpha > beta:
                            break
                return max
            else:
                if agentIndex == state.getNumAgents() - 1:
                    depth -= 1
                    newAgentIndex = 0
                else:
                    newAgentIndex = agentIndex + 1

                min = float('inf')
                for legalAction in state.getLegalActions(agentIndex):
                    successorState = state.generateSuccessor(agentIndex, legalAction)
                    successorScore = minimax(successorState, depth, newAgentIndex, alpha, beta)
                    if successorScore < min:
                        min = successorScore
                    if successorScore < beta:
                        beta = successorScore
                        if beta < alpha:
                            break
                return min

        alpha_ = float('-inf')
        beta_ = float('inf')
        bestAction = None
        for action in gameState.getLegalActions(0):
            score = minimax(gameState.generateSuccessor(0, action), self.depth, 1, alpha_, beta_)
            if score > alpha_:
                alpha_ = score
                bestAction = action
        return bestAction


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    
    def getAction(self, gameState: GameState):
        def expectimax(state, depth, agentIndex):
            if depth == 0 or state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            successorStates = []
            for legalAction in state.getLegalActions(agentIndex):
                successorStates.append(state.generateSuccessor(agentIndex, legalAction))
            if agentIndex == 0:
                scores = [expectimax(successorState, depth, agentIndex + 1) for successorState in successorStates]
                return max(scores)
            else:
                if agentIndex == state.getNumAgents() - 1:
                    depth -= 1
                    agentIndex = 0
                else:
                    agentIndex += 1
                scores = [expectimax(successorState, depth, agentIndex) for successorState in successorStates]
                return sum(scores) / len(scores)

        state = {}

        for action in gameState.getLegalActions(0):
            state[action] = expectimax(gameState.generateSuccessor(0, action), self.depth, 1)

        bestAction = None
        highest = float('-inf')
        for action, score in state.items():
            if score > highest:
                highest = score
                bestAction = action

        return bestAction



def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    score = 0
    pos = currentGameState.getPacmanPosition()
    for ghostState in currentGameState.getGhostStates():
        ghostPosition = ghostState.getPosition()
        ghostDistance = manhattanDistance(ghostPosition, pos)
        if ghostState.scaredTimer <= 0:
            weight = 5
            if ghostDistance > 8:  # too far from pacman, distance don't matter as much
                weight = 0.5
            elif ghostDistance > 2:  # more weights, because ghost is closer to pacman
                weight = 1
            elif ghostDistance >= 0:  # too close to ghost, penalize.
                score -= 100
            score += weight * manhattanDistance(ghostPosition, pos)
            # print(weight, score)
        else:
            score -= 20 * manhattanDistance(ghostPosition, pos)
    # reward pacman for eating capsules; fewer capsules on the map, the better the score.
    capsules = currentGameState.getCapsules()
    score -= len(capsules) * 500

    # reward pacman for going closer to food
    food = currentGameState.getFood()
    foodDistance = [manhattanDistance(pos, food) for food in food.asList()]
    if len(foodDistance) != 0:
        minFoodDistance = min(foodDistance)
        score += 4 / (minFoodDistance + 1)  # the higher the min, the less score pacman gets.
        # score -= 1.5 * minFoodDistance
    # reward pacman for eating food, fewer food on the map, the better the score.
    score -= len(foodDistance) * 20
    # print(score, pos)
    return score



# Abbreviation
better = betterEvaluationFunction
