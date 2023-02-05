import random
from copy import deepcopy
import numpy as np

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']
    
    ### BUILT-IN

    def __init__(self):
    
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        state_copy = deepcopy(state)
        
        drop_phase = True  # TODO: detect drop phase
        
        placed = 0
        for i in range(5):
            for j in range(5):
                if state_copy[i][j] != ' ':
                    placed += 1
        if placed >= 8:
            drop_phase = False
        
        if not drop_phase:
            # TODO: choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            move = []
            val, bestChild = self.max_value(state_copy, 0, self.my_piece)
            for i in range(5):
                for j in range(5):
                    if state_copy[i][j] != bestChild[i][j]:
                        if state_copy[i][j] == ' ':
                            move.insert(0, (i, j))
                        elif bestChild[i][j] == ' ':
                            move.insert(1, (i, j))
            return move

        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better
        move = []
        aiPiece = 0
        for i in range(5):
            for j in range(5):
                if state_copy[i][j] == self.my_piece:
                    aiPiece += 1
        if aiPiece == 0:
            (row, col) = (random.randint(0, 4), random.randint(0, 4))
            while not state[row][col] == ' ':
                (row, col) = (random.randint(0, 4), random.randint(0, 4))
            # ensure the destination (row,col) tuple is at the beginning of the move list
            move.insert(0, (row, col))
            return move
        else:
            val, bestChild = self.max_value(state_copy, 0, self.my_piece)
            for i in range(5):
                for j in range(5):
                    if state_copy[i][j] != bestChild[i][j]:
                        if state_copy[i][j] == ' ':
                            move.insert(0, (i, j))
            return move
        
            
        

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row) + ": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i + 1][col] == state[i + 2][col] == state[i + 3][col]:
                    return 1 if state[i][col] == self.my_piece else -1

        # TODO: check \ diagonal wins
        for row in range(2):
            for col in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row + 1][col + 1] == state[row + 2][col + 2] == state[row + 3][col + 3]:
                    return 1 if state[row][col] == self.my_piece else -1
        # TODO: check / diagonal wins
        for row in range(3, 5):
            for col in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row - 1][col + 1] == state[row - 2][col + 2] == state[row - 3][col + 3]:
                    return 1 if state[row][col] == self.my_piece else -1
        # TODO: check box wins
        for row in range(4):
            for col in range(4):
                if state[row][col] != ' ' and state[row][col] == state[row][col + 1] == state[row + 1][col] == state[row + 1][col + 1]:
                    return 1 if state[row][col] == self.my_piece else -1
                
        return 0  # no winner yet
    
    ### HELPERS
    
    def state_upper_diag(self, state):
        longDiag = []
        shortDiag1 = []
        shortDiag2 = []
        longDiag.extend([state[4][0], state[3][1], state[2][2], state[1][3], state[0][4]])
        shortDiag1.extend([state[4][1], state[3][2], state[2][3], state[1][4]])
        shortDiag2.extend([state[3][0], state[2][1], state[1][2], state[0][3]])
        
        ai = 0
        opp = 0
        
        tempAi = 0
        tempOpp = 0
        for i in longDiag:
            if i == self.my_piece:
                tempAi += 1
            elif i == self.opp:
                tempOpp +=1
                
        tempAi2 = 0
        tempOpp2 = 0
        for i in shortDiag1:
            if i == self.my_piece:
                tempAi2 += 1
            elif i == self.opp:
                tempOpp2 +=1
        
        tempAi3 = 0
        tempOpp3 = 0
        for i in shortDiag2:
            if i == self.my_piece:
                tempAi3 += 1
            elif i == self.opp:
                tempOpp3 +=1
        
        ai = max(tempAi, tempAi2, tempAi3)/4
        opp = max(tempOpp, tempOpp2, tempOpp3)/4
        
        return ai, opp
    
    def state_lower_diag(self, state):
        longDiag = []
        shortDiag1 = []
        shortDiag2 = []
        longDiag.extend([state[0][0], state[1][1], state[2][2], state[3][3], state[4][4]])
        shortDiag1.extend([state[0][1], state[1][2], state[2][3], state[3][4]])
        shortDiag2.extend([state[1][0], state[2][1], state[3][2], state[4][3]])
        
        ai = 0
        opp = 0
        
        tempAi = 0
        tempOpp = 0
        for i in longDiag:
            if i == self.my_piece:
                tempAi += 1
            elif i == self.opp:
                tempOpp +=1
                
        tempAi2 = 0
        tempOpp2 = 0
        for i in shortDiag1:
            if i == self.my_piece:
                tempAi2 += 1
            elif i == self.opp:
                tempOpp2 +=1
        
        tempAi3 = 0
        tempOpp3 = 0
        for i in shortDiag2:
            if i == self.my_piece:
                tempAi3 += 1
            elif i == self.opp:
                tempOpp3 +=1
        
        ai = max(tempAi, tempAi2, tempAi3)/4
        opp = max(tempOpp, tempOpp2, tempOpp3)/4
        
        return ai, opp
    
    def state_horizontal(self, state):
        ai = 0
        opp = 0
        for row in range(5):
            horz = []
            tempAi = 0
            tempOpp = 0
            for col in range(5):
                horz.append(state[row][col])
            for i in horz:
                if i == self.my_piece:
                    tempAi += 1
                elif i == self.opp:
                    tempOpp +=1
            if tempAi > ai:
                ai = tempAi
            if tempOpp > opp:
                opp = tempOpp
        ai = ai/4
        opp = opp/4
        
        return ai, opp
                
            
    
    def state_vertical(self, state):
        ai = 0
        opp = 0
        for col in range(5):
            vert = []
            tempAi = 0
            tempOpp = 0
            for row in range(5):
                vert.append(state[row][col])
            for i in vert:
                if i == self.my_piece:
                    tempAi += 1
                elif i == self.opp:
                    tempOpp +=1
            if tempAi > ai:
                ai = tempAi
            if tempOpp > opp:
                opp = tempOpp
        ai = ai/4
        opp = opp/4
        
        return ai, opp
    
    def state_square(self, state):
        ai = 0
        opp = 0
        
        for row in range(4):
            for col in range(4):
                sqr = []
                tempAi = 0
                tempOpp = 0
                sqr.extend([state[row][col], state[row][col + 1], state[row + 1][col], state[row + 1][col + 1]])
                for i in sqr:
                    if i == self.my_piece:
                        tempAi += 1
                    elif i == self.opp:
                        tempOpp +=1
                if tempAi > ai:
                    ai = tempAi
                if tempOpp > opp:
                    opp = tempOpp
        ai = ai/4
        opp = opp/4
        
        return ai, opp
    
    def succ(self, state, piece):
        drop_phase = True  # TODO: detect drop phase
        placed = 0
        for i in range(5):
            for j in range(5):
                if state[i][j] != ' ':
                    placed += 1
        if placed >= 8:
            drop_phase = False
            
        succ_states = []
        
        if drop_phase == True:
            for i in range(5):
                for j in range(5):
                    if state[i][j] == ' ':
                        tempState = deepcopy(state)
                        tempState[i][j] = piece
                        succ_states.append(tempState)
                        
        elif drop_phase == False:
            for i in range(5):
                for j in range(5):
                    if state[i][j] == piece:
                        for x in range(5):
                            for y in range(5):
                                distance = (i-x)**2 + (j-y)**2
                                if state[x][y] == ' ' and distance <= 2:
                                    tempState = deepcopy(state)
                                    tempState[x][y] = piece
                                    tempState[i][j] = ' '
                                    succ_states.append(tempState)      
            
        return sorted(succ_states)

    def heuristic_game_value(self, state):
        
        if self.game_value(state) != 0:
            return self.game_value(state)
     
        aiScoreDiag, oppScoreDiag = self.state_upper_diag(state)
        aiScoreDiag2, oppScoreDiag2 = self.state_lower_diag(state)
        aiScoreHorz, oppScoreHorz = self.state_horizontal(state)
        aiScoreVert, oppScoreVert = self.state_vertical(state)
        aiScoreSq, oppScoreSq = self.state_square(state)
        
        aiScore = max([aiScoreDiag, aiScoreDiag2, aiScoreHorz, aiScoreVert, aiScoreSq])
        oppScore = max([oppScoreDiag, oppScoreDiag2, oppScoreHorz, oppScoreVert, oppScoreSq])
        
        if aiScore >= oppScore:
            return aiScore
        elif oppScore > aiScore:
            return oppScore*(-1)
    
    
    def max_value(self, state, depth, piece):
        
        if self.game_value(state) != 0:
            return self.game_value(state), state
        
        if depth == 3:
            return self.heuristic_game_value(state), state
        
        if piece == self.my_piece:
            alpha = -np.inf
            succ_states = self.succ(state, piece)
            for i in succ_states:
                alphaTemp, stateTemp = self.max_value(i, depth + 1, self.opp)
                if alphaTemp > alpha:
                    alpha = alphaTemp
                    bestChild = i
            return alpha, bestChild
        
        elif piece == self.opp:
            beta = np.inf
            succ_states = self.succ(state, piece)
            for i in succ_states:
                betaTemp, stateTemp = self.max_value(i, depth + 1, self.my_piece)
                if betaTemp < beta:
                    beta = betaTemp
                    bestChild = i 
            return beta, bestChild
        
        
            
    

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved at " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved from " + chr(move[1][1] + ord("A")) + str(move[1][0]))
            print("  to " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0]) - ord("A")),
                                      (int(move_from[1]), ord(move_from[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
