from keras import models
import numpy as np
import time

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
    player_for_model = 1 if player == 'x' else -1

    # create input tensor
    player_layer = np.full((8, 8), player_for_model)
    input_tensor = np.stack([board_array, player_layer], axis=-1)
    input_tensor = np.expand_dims(input_tensor, axis=0)
    
    # load model
    model = models.load_model('othello_model_full.h5')

    # make prediction about next best move
    predictions = model.predict(input_tensor)
    best_move.value = np.argmax(predictions[0])
