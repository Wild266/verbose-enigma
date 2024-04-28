class Strategy:
    def best_strategy(self, board, player, best_move, still_running, time_limit):
        import time
        start_time = time.time()

        # Helper function to check if a move is legal and count flips
        def is_legal_and_count_flips(index, board, player):
            if board[index] != '.':
                return False, 0
            directions = [1, -1, 8, -8, 7, -7, 9, -9]
            opponent = 'o' if player == 'x' else 'x'
            total_flips = 0
            legal = False

            for direction in directions:
                n = 1
                flips = 0
                while True:
                    ni = index + direction * n
                    if ni < 0 or ni >= len(board) or (ni % 8 == 0 and direction in [1, 9, -7]) or (ni % 8 == 7 and direction in [-1, -9, 7]):
                        break
                    if board[ni] == opponent:
                        flips += 1
                    elif board[ni] == player and flips > 0:
                        total_flips += flips
                        legal = True
                        break
                    else:
                        break
                    n += 1

            return legal, total_flips

        # Main AI logic to select the best move
        best_flips = -1
        candidate_move = None
        for i, cell in enumerate(board):
            if cell == '.':
                legal, flips = is_legal_and_count_flips(i, board, player)
                if legal and flips > best_flips:
                    best_flips = flips
                    candidate_move = i
                    best_move.value = candidate_move  # Update the best move with the current best candidate

        # Handle time limit exceeded case
        if time.time() - start_time > time_limit:
            print("Time limit exceeded while computing the best move.")
            return  # Optionally handle this more gracefully

        # Log the decision
        if candidate_move is not None:
            print(f"AI chose position {candidate_move} with {best_flips} flips.")
        else:
            print("No valid moves found.")


