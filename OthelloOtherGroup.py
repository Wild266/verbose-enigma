

def make_minimax_move(board, player):
   best_score = float('-inf')
   best_move = None
   for move in self.get_legal_moves():
      # Assuming minimax depth and maximizing player initial call
      score = minimax(move, 2, False)
      if score > best_score:
            best_score = score
            best_move = move
   if best_move:
      return best_move

def minimax(move, depth, is_maximizing):
   if depth == 0 or not self.has_legal_move():
      return evaluate_heuristic()
   
   if is_maximizing:
      best_score = float('-inf')
      for new_move in self.get_legal_moves():
            self.board[new_move[0]][new_move[1]] = self.current_player + 1
            score = self.minimax(new_move, depth - 1, False)
            self.board[new_move[0]][new_move[1]] = 0  # Undo move
            best_score = max(best_score, score)
      return best_score
   else:
      best_score = float('inf')
      for new_move in self.get_legal_moves():
            self.board[new_move[0]][new_move[1]] = 1 - self.current_player + 1
            score = self.minimax(new_move, depth - 1, True)
            self.board[new_move[0]][new_move[1]] = 0  # Undo move
            best_score = min(best_score, score)
      return best_score

def evaluate_heuristic(self):
   # Simple stability heuristic: prefer edges and corners
   stability_scores = 0
   corners = [(0, 0), (0, self.n-1), (self.n-1, 0), (self.n-1, self.n-1)]
   for corner in corners:
      if self.board[corner[0]][corner[1]] == self.current_player + 1:
            stability_scores += 3  # corner stability score
      elif self.board[corner[0]][corner[1]] == (1 - self.current_player) + 1:
            stability_scores -= 3
   
   edges = [0, self.n-1]
   for i in range(self.n):
      for edge in edges:
            if self.board[edge][i] == self.current_player + 1 or self.board[i][edge] == self.current_player + 1:
               stability_scores += 1  # edge stability score
            elif self.board[edge][i] == (1 - self.current_player) + 1 or self.board[i][edge] == (1 - self.current_player) + 1:
               stability_scores -= 1
   
   return stability_scores + self.num_tiles[self.current_player] - self.num_tiles[1 - self.current_player]

class Strategy:
   def best_strategy(self, board, player, best_move, still_running, time_limit):
      move = make_minimax_move(board, player)