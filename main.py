import numpy as np
import random

X_wins = 0
O_wins = 0
draws = 0

#This is the random player
class Player:
    def __init__(self, token):
        self.token = token
        
    def make_move(self, board):
        rows, cols = board.shape

        # print("BOARD:",board)
        
        while True:
            col = random.randint(0, cols - 1)  
            if board[0, col] == ' ':
                for row in reversed(range(rows)):
                    if board[row, col] == ' ':
                        board[row, col] = self.token
                        return

#Change this class (now equal to the one obove) and add your strategy here
class Player_Student:
    def __init__(self, token):
        self.token = token
        self.oppToken = 'O' if token == 'X' else 'X'
        
    def make_move(self, board):
        rows, cols = board.shape
        _, col = self.minimax(board, 1, -np.inf, np.inf, self.token)

        if col is not None:
            for row in reversed(range(rows)):
                    if board[row, col] == ' ':
                        board[row, col] = self.token
                        return
        
    def minimax(self, board, depth, alpha, beta, curPlayer):
        if depth == 0 or self.check_winner(self.token, board) or self.check_winner(self.oppToken, board) or self.is_full(board):
            score = self.evaluation(board, curPlayer)
            score -= self.evaluation(board, 'O' if curPlayer == 'X' else 'X')
            
            return score , None
        
        rows, cols = board.shape

        if curPlayer == self.token:
            maxEval = -np.inf
            best_col = None
            for col in [4, 5, 3, 6, 2, 7, 1, 8, 0, 9]:    #pref mid
                if board[0, col] == ' ':
                    for row in reversed(range(rows)):
                        if board[row, col] == ' ':
                            newboard = board.copy()
                            newboard[row,col] = self.token

                            eval, _ = self.minimax(newboard, depth - 1, alpha, beta, self.oppToken)

                            if eval > maxEval:
                                best_col = col

                            maxEval = max(maxEval, eval)
                            alpha = max(alpha, eval)
                            if beta <= alpha: break
            return maxEval, best_col
                            
        else:
            minEval = np.inf
            best_col = None  

            for col in range(cols):
                if board[0, col] == ' ':
                    for row in reversed(range(rows)):
                        if board[row, col] == ' ':
                            newboard = board.copy()
                            newboard[row,col] = self.oppToken

                            eval, _ = self.minimax(newboard, depth - 1, alpha, beta, self.token)

                            if eval < minEval:
                                best_col = col

                            minEval = min(minEval, eval)
                            beta = min(beta, eval)
                            if beta <= alpha: break
            return minEval, best_col                                  

    
    def evaluation(self, board, localToken):
        score = 0

        for row in range(board.shape[0]):
            for col in range(board.shape[1] - 4):
                posLines = board[row, col:col + 5]
                score += self.posLineEvaluation(posLines, localToken)

        for col in range(board.shape[1]):
            for row in range(board.shape[0] - 4):
                posLines = board[row:row + 5, col]
                score += self.posLineEvaluation(posLines, localToken)

        for row in range(board.shape[0] - 4):
            for col in range(board.shape[1] - 4):
                posLines = [board[row + i, col + i] for i in range(5)]
                score += self.posLineEvaluation(posLines, localToken)

        for row in range(4, board.shape[0]):
            for col in range(board.shape[1] - 4):
                posLines = [board[row - i, col + i] for i in range(5)]
                score += self.posLineEvaluation(posLines, localToken)

        return score

    def posLineEvaluation(self, posLine, localToken):
        score = 0
        localOppToken = 'O' if localToken == 'X' else 'X'
        

        numToken = 0
        numOppToken = 0
        numFree = 0
        for i in posLine:
            if i == localToken:
                numToken += 1
            elif i == localOppToken:
                numOppToken += 1
            elif i == ' ':
                numFree += 1


        if numToken == 5:
            score += 5000
        elif numToken == 4 and numFree == 1:
            score += 500
        elif numToken == 3 and numFree == 2:
            score += 200
        elif numToken == 2 and numFree == 3:
            score += 100

        if numOppToken == 4 and numFree == 1:
            score -= 600
        elif numOppToken == 3 and numFree == 2:
            score -= 200
        elif numOppToken == 2 and numFree == 3:
            score -= 100

        return score

        
    def check_winner(self, localToken, board):
        cols = 10
        rows = 10
        winning_length = 5
        # Check horizontal
        for row in range(rows):
            for col in range(cols - winning_length + 1):
                if np.all(board[row, col:col + winning_length] == localToken):
                    return True

        # Check vertical
        for col in range(cols):
            for row in range(rows - winning_length + 1):
                if np.all(board[row:row + winning_length, col] == localToken):
                    return True

        # Check / diagonal 
        for row in range(rows - winning_length + 1):
            for col in range(cols - winning_length + 1):
                if np.all([board[row + i, col + i] == localToken for i in range(winning_length)]):
                    return True

        # Check \ diagonal
        for row in range(winning_length - 1, rows):
            for col in range(cols - winning_length + 1):
                if np.all([board[row - i, col + i] == localToken for i in range(winning_length)]):
                    return True

        return False
    
    def is_full(self, board):
        return np.all(board[0, :] != ' ')


                    
class FiveWins:
    def __init__(self, rows=10, cols=10):
        self.board = np.full((rows, cols), ' ')
        self.rows = rows
        self.cols = cols
        self.winning_length = 5 #5wins

    def print_board(self):
        for row in self.board:
            print('|' + '|'.join(row) + '|')
        print(' ' + ' '.join(str(i) for i in range(self.cols)))

    def check_winner(self, token):
        # Check horizontal
        for row in range(self.rows):
            for col in range(self.cols - self.winning_length + 1):
                if np.all(self.board[row, col:col + self.winning_length] == token):
                    return True

        # Check vertical
        for col in range(self.cols):
            for row in range(self.rows - self.winning_length + 1):
                if np.all(self.board[row:row + self.winning_length, col] == token):
                    return True

        # Check / diagonal 
        for row in range(self.rows - self.winning_length + 1):
            for col in range(self.cols - self.winning_length + 1):
                if np.all([self.board[row + i, col + i] == token for i in range(self.winning_length)]):
                    return True

        # Check \ diagonal
        for row in range(self.winning_length - 1, self.rows):
            for col in range(self.cols - self.winning_length + 1):
                if np.all([self.board[row - i, col + i] == token for i in range(self.winning_length)]):
                    return True

        return False

    def is_full(self):
        return np.all(self.board[0, :] != ' ')

    def play_game(self, player1, player2):
        global X_wins, O_wins, draws
        current_player = player1
        while True:
            current_player.make_move(self.board)
            self.print_board()

            if self.check_winner(current_player.token):
                print(f"Player {current_player.token} wins!")
                if current_player.token == 'X':
                    X_wins += 1
                else:
                    O_wins += 1
                break

            if self.is_full():
                print("Draw game!")
                draws += 1
                break

            current_player = player2 if current_player == player1 else player1

if __name__ == "__main__":   
    for i in range(100):
        player1 = Player('X') #The random player
        player2 = Player_Student('O') #your player
        game = FiveWins()
        game.play_game(player1, player2)
    winrate = O_wins / (O_wins + X_wins + draws)
    print(winrate)