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

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        # score = 1/min(dist from food) - 1/(sum of distances from ghosts) + max(scared Score)/(sum of distances from ghosts if scaredTime > 0)
        capsules = childGameState.getCapsules()
        capsuleScore = 1
        if capsules:
        	capsuleScore = min([util.manhattanDistance(newPos, capsule) for capsule in capsules])


        foodScore = 1
        if newFood.asList():
        	foodScore = min([util.manhattanDistance(newPos, food) for food in newFood.asList()])


		# if foodLocations is not []:
		# 	ghostScore = min(foodLocations)
        ghostScore = 1
        ghostLocations = [util.manhattanDistance(newPos, ghostState.getPosition()) for ghostState in newGhostStates]
        # print(ghostScore, ghostLocations)
        if ghostLocations:
        	ghostScore = min(ghostLocations)
        if ghostScore == 0:
        	ghostScore = 0.0000001

        # print(ghostScore, ghostLocations)

        scaredScore = max(newScaredTimes)
        # print(foodScore, capsuleScore, ghostScore, scaredScore)
        # print('\n')

        return childGameState.getScore() + 1/foodScore + 0.5/capsuleScore  - 1/ghostScore + scaredScore  

def scoreEvaluationFunction(currentGameState):
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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        # """
        # startDepth = 0
        legalActions = gameState.getLegalActions(0)
        # bestAction = legalActions[0]
        # nextState = gameState.getNextState(0, bestAction)
        # maxValue = self.minimaxHelper(1, startDepth, nextState)
        # for i in range(1, len(legalActions)):
        #     currAction = legalActions[i]
        #     nextState = gameState.getNextState(0, currAction)
        #     currValue = self.minimaxHelper(1, startDepth, nextState)
        #     if currValue >  maxValue:
        #         bestAction = currAction

        return max(legalActions, key = lambda action: self.minimaxHelper(1, 0, gameState.getNextState(0, action)))

    def minimaxHelper(self, currAgent, currDepth, currState):
        legalActions = currState.getLegalActions(currAgent)
        if currDepth == self.depth or currState.isLose() or currState.isWin():
            return self.evaluationFunction(currState)
        elif currAgent == 0:
            nextStates = [currState.getNextState(currAgent, action) for action in legalActions]
            return max([self.minimaxHelper(currAgent+1, currDepth, newState) for newState in nextStates])
        else: 
            #print(currAgent, '\n')
            nextStates = [currState.getNextState(currAgent, action) for action in legalActions]
            if currAgent == currState.getNumAgents() - 1:
                return min([self.minimaxHelper(0, currDepth+1, newState) for newState in nextStates])
            return min([self.minimaxHelper(currAgent+1, currDepth, newState) for newState in nextStates])
            



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        return self.alphaBetaHelper(0, 0, gameState, float("-inf"), float("inf"))[1]

    def alphaBetaHelper(self, currAgent, currDepth, currState, alpha, beta):
        legalActions = currState.getLegalActions(currAgent)
        if currDepth == self.depth or currState.isLose() or currState.isWin():
            return (self.evaluationFunction(currState), None)
        
        elif currAgent == 0:
            #newStates = [currState.getNextState(currAgent, action) for action in legalActions]
            bestAction = None
            bestValue = float("-inf")
            for action in legalActions:
                currValue = self.alphaBetaHelper(currAgent+1, currDepth, currState.getNextState(currAgent, action), alpha, beta)[0]
                if bestValue < currValue:
                    bestValue = currValue
                    bestAction = action
                if currValue > beta:
                    return (currValue, action)
                alpha = max(alpha, currValue)
            return (bestValue, bestAction)
        
        else: 
            #print(currAgent, '\n')
            #newStates = [currState.getNextState(currAgent, action) for action in legalActions]
            bestAction = None
            bestValue = float("inf")
            for action in legalActions:
                if currAgent == currState.getNumAgents() - 1:
                    currValue = self.alphaBetaHelper(0, currDepth+1, currState.getNextState(currAgent, action), alpha, beta)[0]
                else:
                    currValue = self.alphaBetaHelper(currAgent + 1, currDepth, currState.getNextState(currAgent, action), alpha, beta)[0]
                if bestValue > currValue:
                    bestValue = currValue
                    bestAction = action
                if currValue < alpha:
                    return (currValue, action)
                beta = min(beta, currValue)
            return (bestValue, bestAction)



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        legalActions = gameState.getLegalActions(0)
        return max(legalActions, key = lambda action: self.expectimaxHelper(1, 0, gameState.getNextState(0, action)))
        

    def expectimaxHelper(self, currAgent, currDepth, currState):
        legalActions = currState.getLegalActions(currAgent)
        if currDepth == self.depth or currState.isLose() or currState.isWin():
            return self.evaluationFunction(currState)
        elif currAgent == 0:
            newStates = [currState.getNextState(currAgent, action) for action in legalActions]
            return max([self.expectimaxHelper(currAgent+1, currDepth, newState) for newState in newStates])
        else: 
            #print(currAgent, '\n')
            newStates = [currState.getNextState(currAgent, action) for action in legalActions]
            if currAgent == currState.getNumAgents() - 1:
                return sum([self.expectimaxHelper(0, currDepth+1, newState) * 1/len(newStates) for newState in newStates])
            return sum([self.expectimaxHelper(currAgent+1, currDepth, newState) * 1/len(newStates) for newState in newStates])

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    
    capsules = currentGameState.getCapsules()
    capsuleScore = 1
    if capsules:
        capsuleScore = min([util.manhattanDistance(newPos, capsule) for capsule in capsules])


    foodScore = 1
    if newFood.asList():
        foodScore = min([util.manhattanDistance(newPos, food) for food in newFood.asList()])


    # if foodLocations is not []:
    #   ghostScore = min(foodLocations)
    ghostScore = 1
    ghostLocations = [util.manhattanDistance(newPos, ghostState.getPosition()) for ghostState in newGhostStates]
    # print(ghostScore, ghostLocations)
    if ghostLocations:
        ghostScore = min(ghostLocations)
    if ghostScore == 0:
        ghostScore = 0.0000001

    # print(ghostScore, ghostLocations)

    scaredScore = max(newScaredTimes)
    # print(foodScore, capsuleScore, ghostScore, scaredScore)
    # print('\n')

    return currentGameState.getScore() + 1/foodScore + 0.5/capsuleScore  - 1/ghostScore + scaredScore  

# Abbreviation
better = betterEvaluationFunction
