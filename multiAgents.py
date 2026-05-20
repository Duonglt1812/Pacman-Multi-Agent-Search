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
        """
        # Trích xuất thông tin hữu ích từ trạng thái tương lai (successor state)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()

        # Khởi tạo điểm số cơ bản
        score = successorGameState.getScore()

        # 1. Thức ăn: Lực hút cơ bản (Sử dụng nghịch đảo khoảng cách)
        foodList = newFood.asList()
        if len(foodList) > 0:
            foodDistances = [util.manhattanDistance(newPos, food) for food in foodList]
            minFoodDist = min(foodDistances)
            score += 1.0 / minFoodDist

        # 2. Ma: Nâng cấp "Giác quan từ xa" và rượt đuổi ma sợ
        for ghostState in newGhostStates:
            ghostPos = ghostState.getPosition()
            distToGhost = util.manhattanDistance(newPos, ghostPos)

            if ghostState.scaredTimer == 0:
                # Ma nguy hiểm
                if distToGhost <= 1:
                    return -999999 # Báo động đỏ: Tránh xa tuyệt đối
                else:
                    # Lực đẩy: Ma càng gần, điểm đánh giá càng bị trừ. Pacman sẽ biết né từ xa.
                    score -= 1.0 / distToGhost
            else:
                # Ma hoảng sợ: Lực hút rượt đuổi
                if distToGhost > 0:
                    score += 2.0 / distToGhost

        # 3. Chống lười biếng: Phạt nặng nếu chọn đứng im
        from game import Directions
        if action == Directions.STOP:
            score -= 50

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
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
        numAgents = gameState.getNumAgents()
        
        
        def minimax(state, agentIndex, depth):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            legalActions = state.getLegalActions(agentIndex)
            if not legalActions:
                return self.evaluationFunction(state)

            nextAgent = agentIndex + 1
            nextDepth = depth

            if nextAgent == numAgents :
                nextAgent = 0
                nextDepth = depth + 1

            values = []
            for action in legalActions:
                successor = state.generateSuccessor(agentIndex, action)
                value = minimax(successor, nextAgent, nextDepth)
                values.append(value)

            if agentIndex == 0:
                return max(values)
            else:
                return min(values)

        bestAction = None
        bestValue = float("-inf")

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            value = minimax(successor, 1, 0)

            if value > bestValue:
                bestValue = value
                bestAction = action

        return bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def alphaBeta(self, state: GameState, depth: int, agentIndex: int, alpha: float, beta: float):
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)

        numAgents = state.getNumAgents()
        nextAgentIndex = (agentIndex + 1) % numAgents
        nextDepth = depth + 1 if nextAgentIndex == 0 else depth

        legalActions = state.getLegalActions(agentIndex)
        if len(legalActions) == 0:
            return self.evaluationFunction(state)

        if agentIndex == 0:
            value = float('-inf')
            for action in legalActions:
                successor = state.generateSuccessor(agentIndex, action)
                value = max(value, self.alphaBeta(successor, nextDepth, nextAgentIndex, alpha, beta))
                alpha = max(alpha, value)
                if alpha > beta:
                    break
            return value

        else:
            value = float('inf')
            for action in legalActions:
                successor = state.generateSuccessor(agentIndex, action)
                value = min(value, self.alphaBeta(successor, nextDepth, nextAgentIndex, alpha, beta))
                beta = min(beta, value)
                if beta < alpha:
                    break
            return value

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        alpha = float('-inf')
        beta = float('inf')
        bestAction = Directions.STOP
        bestValue = float('-inf')

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            value = self.alphaBeta(successor, 0, 1, alpha, beta)
            if value > bestValue:
                bestValue = value
                bestAction = action
            alpha = max(alpha, value)
        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def expectimax(self, state: GameState, depth: int, agentIndex: int):
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)
        
        numAgents = state.getNumAgents()
        nextAgentIndex = (agentIndex + 1) % numAgents
        nextDepth = depth + 1 if nextAgentIndex == 0 else depth

        if agentIndex == 0:
            legalActions = state.getLegalActions(agentIndex)
            if len(legalActions) == 0:
                return self.evaluationFunction(state)
            value = float('-inf')
            for action in legalActions:
                successor = state.generateSuccessor(agentIndex, action)
                value = max(value, self.expectimax(successor, nextDepth, nextAgentIndex))
            return value
            
        else:
            totalValue = 0
            legalActions = state.getLegalActions(agentIndex)
            numActions = len(legalActions)

            if numActions == 0:
                return self.evaluationFunction(state)
            
            for action in legalActions:
                successor = state.generateSuccessor(agentIndex, action)
                totalValue += self.expectimax(successor, nextDepth, nextAgentIndex)
            return totalValue / numActions
        
    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        bestAction = Directions.STOP
        bestValue = float('-inf')
        legalActions = gameState.getLegalActions(0)

        for action in legalActions:
            successor = gameState.generateSuccessor(0, action)
            value = self.expectimax(successor, 0, 1)
            if value > bestValue:
                bestValue = value
                bestAction = action
        return bestAction

def betterEvaluationFunction(currentGameState: GameState):
    """
    Extreme evaluation function for Q5
    """
    # điểm số thắng/thua:
    # nếu thắng thì trả về vô cùng dương

    if currentGameState.isWin():
        return float('inf')

    # nếu thua thì trả về vô cùng âm
    if currentGameState.isLose():
        return float('-inf')
    
    # lấy thông tin từ trạng thái hiện tại

    pos = currentGameState.getPacmanPosition() # vị trí của pacman
    food = currentGameState.getFood().asList() # danh sách vị trí thức ăn còn lại
    ghosts = currentGameState.getGhostStates() # danh sách trạng thái ghost
    capsules = currentGameState.getCapsules() # danh sách vị trí điểm đặc biệt còn lại

    score = currentGameState.getScore() # điểm số hiện tại

    # FOOD
    if food:
         # tính khoảng cách Manhattan từ pacman đến từng thức ăn còn lại
        foodDistances = [manhattanDistance(pos, f) for f in food] 

        nearestFood = min(foodDistances) # lấy ra khoảng cách nhỏ nhất

        # khuyến khích pacman di chuyển về phía thức ăn gần nhất, 
        # cộng thêm 15 điểm chia cho khoảng cách đến thức ăn đó (cộng 1 để tránh chia cho 0)
        score += 15.0 / (nearestFood + 1)

        # khuyến khích dọn dẹp bảng thức ăn, trừ đi 4 điểm cho mỗi thức ăn còn lại
        score -= 4 * len(food)


    # CAPSULES
    # trừ đi 20 điểm cho mỗi điểm đặc biệt còn lại để khuyến khích pacman ăn chúng
    score -= 20 * len(capsules)


    # GHOSTS
    for ghost in ghosts:
        ghostPos = ghost.getPosition() # lấy vị trí của ghost
        dist = manhattanDistance(pos, ghostPos) # tính khoảng cách Manhattan từ pacman đến ghost

        if ghost.scaredTimer > 0:
            # nếu đang trong thời gian ăn viên đặc biệt, 
            # khuyến khích pacman di chuyển tới ghost để ăn chúng, 
            # cộng thêm 25 điểm chia cho khoảng cách đến ghost đó (cộng 1 để tránh chia cho 0)
            score += 25.0 / (dist + 1)

        else:
            # khuyến khích pacman tránh xa ghost, trừ đi 1000 điểm nếu ghost quá gần (khoảng cách <= 1),
            if dist <= 1:
                score -= 1000
            
            # nếu ghost ở xa, trừ đi 4 điểm chia cho khoảng cách đến ghost đó để khuyến khích pacman tránh xa chúng
            else:
                score -= 4.0 / dist

    return score

# Abbreviation
better = betterEvaluationFunction
