# Aknazar Janibek Othello Agent
import time

class Strategy:
    DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    def __init__(self):
        self.board = None

    def best_strategy(self, board, player, best_move, still_running, time_limit):
        if self.board is None:
            board = [list(board[i:i+8]) for i in range(0, 64, 8)]
        moves = self.valid_moves(board, player)
        if not moves:
            best_move.value = None
        else:
            best_move.value = self.mcts(board, moves, player, time_limit, time.time())

    def mcts(self, board, moves, player, time_limit, start_time):
        best_score = float('-inf')
        best_move = None
        for move in moves:
            score = self.simulate_move(board, move, player, time_limit / len(moves), start_time)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move[0] * 8 + best_move[1] if best_move else None

    def simulate_move(self, board, move, player, allocated_time, start_time):
        score = 0
        trials = 0
        target_trials = 500
        while trials < target_trials:
            score += self.simulate(board, move, player)
            trials += 1
        return score / trials if trials > 0 else 0

    def simulate(self, board, move, player):
        simulated_board = [row[:] for row in board]
        r, c = move
        simulated_board[r][c] = player
        self.apply_move(simulated_board, player, move)
        return self.evaluate_board(simulated_board, player)

    def apply_move(self, board, player, move):
        for dr, dc in self.DIRECTIONS:
            self.flip_tokens(board, move, dr, dc, player)

    def flip_tokens(self, board, move, dr, dc, player):
        r, c = move
        r += dr
        c += dc
        to_flip = []
        while 0 <= r < 8 and 0 <= c < 8 and board[r][c] not in ('.', player):
            to_flip.append((r, c))
            r += dr
            c += dc
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
            for (fr, fc) in to_flip:
                board[fr][fc] = player

    def valid_moves(self, board, player):
        opponent = 'o' if player == 'x' else 'x'
        moves = []
        for r in range(8):
            for c in range(8):
                if board[r][c] == '.' and any(self.is_valid_move(board, r, c, dr, dc, player, opponent) for dr, dc in self.DIRECTIONS):
                    moves.append((r, c))
        return moves

    def is_valid_move(self, board, r, c, dr, dc, player, opponent):
        r += dr
        c += dc
        has_opponent = False
        while 0 <= r < 8 and 0 <= c < 8:
            if board[r][c] == opponent:
                has_opponent = True
                r += dr
                c += dc
            elif board[r][c] == player and has_opponent:
                return True
            else:
                break
        return False

    def evaluate_board(self, board, player):
        opponent = 'o' if player == 'x' else 'x'
        score_values = {'corner': 1, 'edge': 1, 'other': 1}
        player_score = 0
        opponent_score = 0

        for r in range(8):
            for c in range(8):
                if board[r][c] == player:
                    if (r, c) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
                        player_score += score_values['corner']
                    elif r in [0, 7] or c in [0, 7]:
                        player_score += score_values['edge']
                    else:
                        player_score += score_values['other']
                elif board[r][c] == opponent:
                    if (r, c) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
                        opponent_score += score_values['corner']
                    elif r in [0, 7] or c in [0, 7]:
                        opponent_score += score_values['edge']
                    else:
                        opponent_score += score_values['other']

        return player_score - opponent_score