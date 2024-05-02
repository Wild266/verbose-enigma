import copy

directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

def is_on_board(x, y):
   """Check if the (x, y) coordinates are on the board."""
   return 0 <= x < 8 and 0 <= y < 8

def is_legal_move(board, move, player):
   """Check if a move is legal for the given player on the board."""
   x, y = move
   if board[x][y] != 0:
      return False  # Cell is not empty

   for dx, dy in directions:
      nx, ny = x + dx, y + dy
      has_opponent_piece = False
      while is_on_board(nx, ny) and board[nx][ny] != 0 and board[nx][ny] != player:
         nx += dx
         ny += dy
         if is_on_board(nx, ny) and board[nx][ny] == player:
            has_opponent_piece = True
            break
      if has_opponent_piece:
         return True
   return False

def get_legal_moves(board, player):
   moves = []
   for i in range(8):
      for j in range(8):
         move = (i, j)
         if is_legal_move(board, move, player):
            moves.append(i, j)

def count_tiles(board, player):
   tiles = 0
   for i in range(8):
      for j in range(8):
         if board[i][j] == player:
            tiles += 1
   return tiles

def make_minimax_move(board, player):
   best_score = float('-inf')
   best_move = None
   # copy board for the minimax algorithm to avoid modifying original board
   temp_board = copy.deepcopy(board)
   for move in get_legal_moves(temp_board, player):
      # Assuming minimax depth and maximizing player initial call
      score = minimax(move, temp_board, player, 2, False)
      if score > best_score:
            best_score = score
            best_move = move
   if best_move:
      return best_move

def minimax(move, board, player, depth, is_maximizing):
   if depth == 0 or len(get_legal_moves(board, player)) == 0:
      return evaluate_heuristic()
   
   if is_maximizing:
      best_score = float('-inf')
      for new_move in get_legal_moves(board, player):
         old_state = board[new_move[0]][new_move[1]]
         board[new_move[0]][new_move[1]] = player
         score = minimax(new_move, board, player, depth - 1, False)
         board[new_move[0]][new_move[1]] = old_state # Undo State
         best_score = max(best_score, score)
      return best_score
   else:
      best_score = float('inf')
      for new_move in get_legal_moves():
         old_state = board[new_move[0]][new_move[1]]
         board[new_move[0]][new_move[1]] = player
         score = minimax(new_move, depth - 1, True)
         board[new_move[0]][new_move[1]] = old_state  # Undo move
         best_score = min(best_score, score)
      return best_score

def evaluate_heuristic(board, player):
   # Simple stability heuristic: prefer edges and corners
   stability_scores = 0
   corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
   for corner in corners:
      if board[corner[0]][corner[1]] == player:
         stability_scores += 3  # corner stability score
      elif board[corner[0]][corner[1]] == (1 - player) + 1:
         stability_scores -= 3
   
   edges = [0, 7]
   for i in range(8):
      for edge in edges:
            if board[edge][i] == player or board[i][edge] == player:
               stability_scores += 1  # edge stability score
            elif board[edge][i] == (-player) + 1 or board[i][edge] == (-player) + 1:
               stability_scores -= 1

   num_player_tiles = count_tiles(board, player)
   num_opponent_tiles = count_tiles(board, -player)

   return stability_scores + num_player_tiles - num_opponent_tiles

class Strategy:
   def best_strategy(self, board, player, best_move, still_running, time_limit):
      move = make_minimax_move(board, player)
      if move:
         row, col = move
         best_move.value = (row * 8) + col
