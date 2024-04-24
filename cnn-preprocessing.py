import pandas as pd
import numpy as np

directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

def move_to_index(move):
    """ Convert board notation to index."""
    idx = (int(move[1]) - 1, ord(move[0]) - ord('a'))
    return idx

def apply_move(board, move, player):
    """ Apply a move to the board, assuming the move is valid. """
    x, y = move_to_index(move)
    board[x][y] = player

    # Flip opponent's pieces
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        pieces_to_flip = []
        while 0 <= nx < 8 and 0 <= ny < 8 and board[nx][ny] == -player:
            pieces_to_flip.append((nx, ny))
            nx += dx
            ny += dy
        if 0 <= nx < 8 and 0 <= ny < 8 and board[nx][ny] == player:
            for px, py in pieces_to_flip:
                board[px][py] = player

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

def string_to_board_states(moves, winner):
    """ Generate board states from a move string."""
    initial_board = [[0]*8 for _ in range(8)]
    initial_board[3][3] = initial_board[4][4] = -1  # White
    initial_board[3][4] = initial_board[4][3] = 1  # Black
    board_states = []
    player = 1  # Black moves first
    current_board = [row[:] for row in initial_board]

    for i in range(0, len(moves), 2):
      y_probabilities = [[0]*8 for _ in range(8)]
      move = moves[i:i+2]

      if is_legal_move(current_board, move_to_index(move), player):
        pass
      else:
        # player can't play, so this move is made by the other player
        player = -player
        if not is_legal_move(current_board, move_to_index(move), player):
          break

      x, y = move_to_index(move)
      if player == winner:
        y_probabilities[x][y] = 1.0
      else:
        # assign equal probabilities to all other legal moves for player
        num_legal_moves = 0
        for p in range(8):
          for q in range(8):
            if (p != x and q != y) and is_legal_move(current_board, (p,q), player):
              y_probabilities[p][q] = 1
              num_legal_moves += 1

        if num_legal_moves > 0:
          y_probabilities = (np.array(y_probabilities) / num_legal_moves).tolist()
        else:
          y_probabilities[x][y] = 1.0

      board_states.append(([row[:] for row in current_board], player, y_probabilities))
      
      # now apply the move and switch players to move on to the next state
      apply_move(current_board, move, player)
      player = -player

    return board_states

def pretty_print_board(board):
    # Pretty-print the board
    for i in range(8):
        print(str(i+1) + ' ', end='')  # Print the row number
        for j in range(8):
            piece = board[i][j]
            if piece == 1:
                print('B', end=' ')
            elif piece == -1:
                print('W', end=' ')
            else:
                print('.', end=' ')
        print()
    print('  a b c d e f g h')

# preprocess dataset
games = pd.read_csv('othello_dataset.csv')
output = []
for index, row in games.iterrows():
  print(f"Starting Game {index+1}/{len(games)}")
  moves = row['game_moves']
  winner = row['winner']
  board_states = string_to_board_states(moves, winner)
  output += board_states

output_df = pd.DataFrame(output, columns=['X', 'player', 'y'])
output_df.to_csv('preprocessed_dataset.csv', index=False)
