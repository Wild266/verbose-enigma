import random
import time

class MonteCarloStrategy:
    def best_strategy(self, board, player, best_move, still_running, time_limit):
        start_time = time.time()
        board = [list(board[i:i+8]) for i in range(0, 64, 8)]
        moves = self.valid_moves(board, player)
        if not moves:
            best_move.value = None
        else:
            best_move.value = self.monte_carlo_search(board, moves, player, time_limit, start_time)

    def monte_carlo_search(self, board, moves, player, time_limit, start_time):
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
        while time.time() - start_time < allocated_time and trials < 50:
            score += self.simulate(board, move, player)
            trials += 1
        return score / trials if trials > 0 else 0

    def simulate(self, board, move, player):
        simulated_board = [row[:] for row in board]
        r, c = move
        simulated_board[r][c] = player
        self.apply_move(simulated_board, player, move)
        score = self.evaluate_board(simulated_board, player)
        return score

    def apply_move(self, board, player, move):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
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
                if board[r][c] == '.' and any(self.is_valid_direction(board, r, c, dr, dc, player, opponent) for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]):
                    moves.append((r, c))
        return moves

    def is_valid_direction(self, board, r, c, dr, dc, player, opponent):
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
        player_score = 0
        opponent_score = 0
        corner_value = 25
        edge_value = 5

        # Evaluate corners
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        for r, c in corners:
            if board[r][c] == player:
                player_score += corner_value
            elif board[r][c] == opponent:
                opponent_score += corner_value        # Evaluate edges, excluding the corners
        for c in range(1, 7):
            if board[0][c] == player:
                player_score += edge_value
            elif board[0][c] == opponent:
                opponent_score += edge_value
            if board[7][c] == player:
                player_score += edge_value
            elif board[7][c] == opponent:
                opponent_score += edge_value

        for r in range(1, 7):
            if board[r][0] == player:
                player_score += edge_value
            elif board[r][0] == opponent:
                opponent_score += edge_value
            if board[r][7] == player:
                player_score += edge_value
            elif board[r][7] == opponent:
                opponent_score += edge_value

        # Evaluate all other squares
        for r in range(8):
            for c in range(8):
                if board[r][c] == player:
                    player_score += 1
                elif board[r][c] == opponent:
                    opponent_score += 1

        return player_score - opponent_score

