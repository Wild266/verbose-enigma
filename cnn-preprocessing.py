import pandas as pd

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
    x, y = move_to_index(move)
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

def string_to_board_states(moves):
    """ Generate board states from a move string."""
    initial_board = [[0]*8 for _ in range(8)]
    initial_board[3][3] = initial_board[4][4] = -1  # White
    initial_board[3][4] = initial_board[4][3] = 1  # Black
    board_states = []
    board_states.append(initial_board)

    current_board = [row[:] for row in initial_board]
    player = 1  # Black moves first

    for i in range(0, len(moves), 2):
        move = moves[i:i+2]
        if is_legal_move(current_board, move, player):
          apply_move(current_board, move, player)
        else:
          player = -player
          if not is_legal_move(current_board, move, player):
            break
          else:
            apply_move(current_board, move, player)
        board_states.append([row[:] for row in current_board])
        player = -player  # Switch player

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


def generate_states(moves, winner):
  """ Generate all intermediate states from a game and the final outcome. """
  board_states = string_to_board_states(moves)
  results = []
  for state in board_states:
    state_key = str(state)  # Convert the state to a string to use as a dictionary key
    results.append((state_key, winner))
  return results

def calculate_win_probabilities(games):
    """ Calculate the win probabilities for all states in all games. """
    state_results = {}
    
    for _, game in games.iterrows():
      moves = game['game_moves']
      winner = int(game['winner'])
      results = generate_states(moves, winner)
      for state_key, result in results:
        if state_key not in state_results:
          state_results[state_key] = {'wins': 0, 'losses': 0, 'draws': 0, 'total': 0}
        
        if result == 1:  # Win for black
          state_results[state_key]['wins'] += 1
        elif result == -1:  # Win for white
          state_results[state_key]['losses'] += 1
        else:  # Draw
          state_results[state_key]['draws'] += 1
        
        state_results[state_key]['total'] += 1

    # Calculate probabilities
    for state_key in state_results.keys():
      state_info = state_results[state_key]
      win_prob = state_info['wins'] / state_info['total'] if state_info['total'] > 0 else 0
      state_results[state_key]['win_prob'] = win_prob

    return state_results

games = pd.read_csv('othello_dataset.csv')
game_id, winner, moves_str = games.iloc[0]
state_probabilities = calculate_win_probabilities(games.head())
print(len(state_probabilities))
# board_states = string_to_board_states(moves_str)
