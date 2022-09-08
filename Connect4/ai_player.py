from player import Player
import numpy as np
from copy import deepcopy
from game import Game
import utils
import re 


class AIPlayer(Player):
    """This player should implement a heuristic along with a min-max and alpha
    beta search to """
	
    def __init__(self):
        self.name = "SirADN"
        self.depth = 2 # profondeur maximale au-delà de la laquelle on évaluera l'utilité avec une heuristique
        self.width = 7
        self.height = 6
        self.winning_length = 4
        self.players = [-1, 1]
    
    def getColumn(self, board):
         # TODO(student): implement this!
        action = self.getActionAlphaBeta(board)
        return action

    #**********************************#
    # Utils
    def getLegalActions(self, board):
        return board.getPossibleColumns()
    
    def generateSuccessor(self, board, action, agentIndex):
        board_copy = deepcopy(board)
        board_copy.play(agentIndex, action)
        return board_copy

    # fonction qui calcule s'il y a un winner ou non et le renvoie : renvoie None si pas de winner 
    def getWinner(self, board):
        for x in range (self.width):
            for y in range (self.height):
                tests = []
                tests.append(board.getCol(x))
                tests.append(board.getRow(y))
                tests.append(board.getDiagonal(True, x - y))
                tests.append(board.getDiagonal(False, x + y))
                for test in tests:
                    color, size = utils.longest(test)
                    if size >= self.winning_length:
                        for player in self.players:
                            if player == color:
                                return player

    def heuristic(self, board):
        #print(board)
        #return 0
        # on évalue si on a un gagnant
        winner = self.getWinner(board)
        if winner is not None: 
            if winner == self.color:
                return np.inf
            else: 
                return -np.inf
        # sinon on calcule l'heuristique

        roles = ('ai', 'ad')

        # on calcule le nombre de pions tout seul de chaque joueur, pondérés par leur endroit sur la grille 
        ones = {'ai': 0, 'ad': 0}
        for col in range(self.width): 
            height = board.getHeight(col)
            col_list = board.getCol(col)
            for x in col_list: 
                if x != 0 :
                    if x == self.color : 
                        ones['ai'] += (4 - abs(3-col))
                    else : 
                        ones['ad'] += (4 - abs(3-col))
        
        heur_ones = ones['ai'] - ones['ad']         

        patterns = {'ai': {'col': [], 'row': [], 'diag': []}, 'ad': {'col': [], 'row': [], 'diag': []}}

        # **************************************************************** 
        # Colonnes
        # Motifs intéressant dans les colonnes 
        if self.color == 1: 
            patterns['ai']['col'] = [(2, '1100'), (3, '1110')]
            patterns['ad']['col'] = [(2, '-1-100'), (3, '-1-1-10')]
        elif self.color == -1:
            patterns['ad']['col'] = [(2, '1100'), (3, '1110')]
            patterns['ai']['col'] = [(2, '-1-100'), (3, '-1-1-10')]

        # Traitement de ces motifs dans les colonnes 
        cols = {'ai': 0, 'ad': 0}
        for col_num in range (self.width):
            col = board.getCol(col_num)
            char = ''
            for x in col : 
                char += str(x)
            for role in roles: 
                for pattern in patterns[role]['col']:
                    #print(f"char : {char}")
                    #print(f"pattern : {pattern[1]}")
                    if re.search(pattern[1], char) :
                        cols[role] += pattern[0]
        # Calcul du nombre de patterns retrouvés 
        heur_cols = cols['ai'] - cols['ad']

        # **************************************************************** 
        # Rows 
        # Motifs intéressant dans les rows 
        if self.color == 1: 
            patterns['ai']['row'] = [(2, '1100'), (2, '1010'), (2, '1001'), (2, '0110'), (2, '0101'), (2, '0011'), (3, '1110'), (3, '1011'), (3, '1101'), (3, '0111')]
            patterns['ad']['row'] = [(2, '-1-100'), (2, '-10-10'), (2, '-100-1'), (2, '0-1-10'), (2, '0-10-1'), (2, '00-1-1'), (3, '-1-1-10'), (3, '-10-1-1'), (3, '-1-10-1'), (3, '0-1-1-1')]
        elif self.color == -1: 
            patterns['ad']['row'] = [(2, '1100'), (2, '1010'), (2, '1001'), (2, '0110'), (2, '0101'), (2, '0011'), (3, '1110'), (3, '1011'), (3, '1101'), (3, '0111')]
            patterns['ai']['row'] = [(2, '-1-100'), (2, '-10-10'), (2, '-100-1'), (2, '0-1-10'), (2, '0-10-1'), (2, '00-1-1'), (3, '-1-1-10'), (3, '-10-1-1'), (3, '-1-10-1'), (3, '0-1-1-1')]
        
        # Traitement de ces motifs dans les rows 
        rows = {'ai': 0, 'ad': 0}
        for row_num in range (self.height):
            row = board.getRow(row_num)
            if 0 in row and row != [0, 0, 0, 0, 0, 0, 0]:
                char = ''
                for x in row : 
                    char += str(x)
                for role in roles:
                    for pattern in patterns[role]['row']:
                        #print(f"char : {char}")
                        #print(f"pattern : {pattern[1]}")
                        if re.search(pattern[1], char) :
                            rows[role] += pattern[0]
        # Calcul du nombre de patterns retrouvés 
        heur_rows = rows['ai'] - rows['ad']

        heur = heur_ones + heur_cols + heur_rows
        return heur


        # patterns de rows 



        # on calcule le nombre de pions de deux pour chaque joueur : !!!!!!! il faut les pondérer par leur endroit sur la grille 
        """ cols = {str(self.color): 0, str(-self.color): 0}
        rows = {str(self.color): 0, str(-self.color): 0}
        diag_up = {str(self.color): 0, str(-self.color): 0}
        diag_down = {str(self.color): 0, str(-self.color): 0}

        for col in range (self.width):
            cols[str(col)] = board.getCol(col)

        for row in range (self.height):
            rows[str(row)] = board.getRow(row)

        for col in range (self.width):
            for row in range (self.height):
                diag_up[col] = board.getDiagonal(True, col - row)
                diag_down[col] = board.getDiagonal(False, col + row)

        for test in tests:
            color, size = utils.longest(test)
            if size >= self.winning_length:
                for player in self.players:
                    if player == color:
                        return player
        pass """

    #**********************************#
    # AlphaBeta
    def getActionAlphaBeta(self, board):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        return self.alpha_beta_max_value(board)[1]

    # définition de max_value()
    def alpha_beta_max_value(self, board, depth=0, alpha=-np.inf, beta=np.inf):
        maxVal = -np.inf 
        bestAction = None
        # On cherche toutes les actions possibles depuis cet état 
        legalMoves = self.getLegalActions(board)
        # On  évalue la condition de terminaison
        if depth == self.depth or len(legalMoves) == 0 or self.getWinner(board) is not None :
            return self.heuristic(board), None
        # On poursuit l'implémentation de max_value() 
        for action in legalMoves :
            successorBoard = self.generateSuccessor(board, action, self.color)
            value = self.alpha_beta_min_value(successorBoard, depth +1, alpha, beta)[0]
            if value is not None and value > maxVal :
                maxVal = value
                bestAction = action
            # alpha-beta pruning : si v > beta, on s'arrête là
            if value > beta : 
                return value, action
            # alpha-beta pruning : il faut metter à jour alpha 
            alpha = max(alpha,value)
        return maxVal, bestAction
        
    # définition de min_value()
    def alpha_beta_min_value(self, board, depth=0, alpha=-np.inf, beta=np.inf):
        minVal = np.inf 
        bestAction = None
        # On cherche toutes les actions possibles depuis cet état 
        legalMoves = self.getLegalActions(board)
        # On  évalue la condition de terminaison
        if depth == self.depth or len(legalMoves) == 0 or self.getWinner(board) is not None :
            return self.heuristic(board), None
        # On poursuit l'implémentation de min_value() 
        for action in legalMoves :
            successorBoard = self.generateSuccessor(board, action, -self.color)
            value = self.alpha_beta_max_value(successorBoard, depth +1, alpha, beta)[0]
            if value is not None and value < minVal :
                minVal = value
                bestAction = action
            # alpha-beta pruning : si v < alpha, on s'arrête là
            if value < alpha : 
                return value, action
            # alpha-beta pruning : il faut metter à jour beta 
            beta = min(beta,value)
        return minVal, bestAction



    #**********************************#
    # MinMax
    def getActionMinMax(self, board):
        # ! à changer suivant la personne par laquelle on commence !!!
        maxVal = -np.inf 
        bestAction = None
        for action in self.getLegalActions(board) :
            successorBoard = self.generateSuccessor(board, action, self.color)
            value = self.min_value(successorBoard)
            if value is not None and value > maxVal :
                bestAction = action
                maxVal = value
        return bestAction

    # définition de max_value()
    def max_value(self, board, depth=0):
        maxVal = -np.inf 
        # On cherche toutes les actions possibles depuis cet état 
        legalMoves = self.getLegalActions(board) 
        # On  évalue la condition de terminaison        
        if depth == self.depth or len(legalMoves) == 0 or self.getWinner(board) is not None :
            return self.heuristic(board)
        # On poursuit l'implémentation de max_value() en gardant en tête qu'on arrive sur le premier Ghost 
        for action in legalMoves :
            successorBoard = self.generateSuccessor(board, action, self.color)
            value = self.min_value(successorBoard, depth)
            if value is not None and value > maxVal :
                maxVal = value
        return maxVal
        
    # définition de min_value()
    def min_value(self, board, depth=0):
        minVal = np.inf 
        # On cherche toutes les actions possibles depuis cet état 
        legalMoves = self.getLegalActions(board) 
        # On  évalue la condition de terminaison
        if depth == self.depth or len(legalMoves) == 0 or self.getWinner(board) is not None :
            return self.heuristic(board)
        # On poursuit l'implémentation de min_value() en gardant en tête que le prochain agent est soit Pacman soit un Ghost
        for action in legalMoves :
            successorBoard = self.generateSuccessor(board, action, -self.color)
            value = self.max_value(successorBoard, depth +1)
            if value is not None and value < minVal :
                minVal = value
        return minVal

