from keras import models
import numpy as np
import time

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

class Strategy:
  def best_strategy(self, board, player, best_move, still_running, time_limit):
    start_time = time.time()

    # convert board and player strings to numbers to be passed to model
    board_array = np.zeros((8, 8))
    count = 0
    for i in range(8):
      for j in range(8):
        if board[count] == 'x':
          board_array[i][j] = 1
        elif board[count] == 'o':
          board_array[i][j] = -1
        count += 1
    player_for_model = 1 if player == 'x' else -1

    # create input tensor
    player_layer = np.full((8, 8), player_for_model)
    input_tensor = np.stack([board_array, player_layer], axis=-1)
    input_tensor = np.expand_dims(input_tensor, axis=0)
    
    # load model
    model = models.load_model('othello_model_full.h5')

    # make prediction about next best move
    predictions = model.predict(input_tensor)[0]

    # loop through output probabilities until a legal move is found
    while True:
      move = np.argmax(predictions)
      row, col = move // 8, move % 8
      if is_legal_move(board_array, [row, col], player_for_model):
        best_move.value = move
        break
      else:
        predictions[move] = 0

