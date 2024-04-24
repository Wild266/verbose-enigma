import pandas as pd

def move_to_index(move):
  """ Convert board notation to index."""
  return (ord(move[0]) - ord('a'), int(move[1]) - 1)

def move_to_index(move):
    # Convert move notation to board indices
    col = ord(move[0]) - ord('a')
    row = 8 - int(move[1])  # The board is printed with row 1 at the bottom
    return row, col

def on_board(x, y):
    # Check if the position is on the board
    return 0 <= x < 8 and 0 <= y < 8

def apply_move(board, move, player):
    # Apply a move and flip the pieces
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    row, col = move_to_index(move)
    board[row][col] = player  # Place the piece

    for dr, dc in directions:
        r, c = row + dr, col + dc
        pieces_to_flip = []
        while on_board(r, c) and board[r][c] == -player:
            pieces_to_flip.append((r, c))
            r += dr
            c += dc

        if on_board(r, c) and board[r][c] == player:
            for pr, pc in pieces_to_flip:
                board[pr][pc] = player

    return board

def string_to_board_states(moves):
  """ Generate board states from a move string."""
  initial_board = [[0]*8 for _ in range(8)]
  initial_board[3][3] = initial_board[4][4] = 1
  initial_board[3][4] = initial_board[4][3] = -1
  board_states = []
  
  current_board = [row[:] for row in initial_board]
  player = -1  # Black moves first

  for i in range(0, len(moves), 2):
    move = moves[i:i+2]
    apply_move(current_board, move, player)
    board_states.append([row[:] for row in current_board])
    player = -player  # Switch player

  return board_states

def pretty_print_board(board):
    # Pretty-print the board
    print('  a b c d e f g h')
    for i in range(8):
        print(str(8 - i) + ' ', end='')  # Print the row number
        for j in range(8):
            piece = board[i][j]
            if piece == 1:
                print('W', end=' ')
            elif piece == -1:
                print('B', end=' ')
            else:
                print('.', end=' ')
        print()

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
    
    for moves, winner in games:
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
# state_probabilities = calculate_win_probabilities(list(games['game_moves']))
print(moves_str)
board_states = string_to_board_states(moves_str)
print(game_id)
pretty_print_board(board_states[-1])
