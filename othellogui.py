import pygame
from pygame.locals import *
from OthelloTJsiteh import Strategy
import threading
import sys
import time
# Define constants

TIME_LIMIT = 5
CELL_SIZE = 60
ROWS, COLS = 8, 8
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WIDTH, HEIGHT = CELL_SIZE*ROWS, CELL_SIZE*COLS

class StoppableThread(threading.Thread):
    def __init__(self, *args, time_limit, **kwargs):
        self.time_limit = time_limit
        self._run_backup = self.run  # Save superclass run() method.
        self.run = self._run  # Change it to custom version.
        super().__init__(*args, **kwargs)

    def _run(self):
        self.start_time = time.time()
        sys.settrace(self.globaltrace)
        self._run_backup()  # Call superclass run().
        self.run = self._run_backup  # Restore original.

    def globaltrace(self, frame, event, arg):
        return self.localtrace if event == 'call' else None

    def localtrace(self, frame, event, arg):
        if(event == 'line' and
           time.time()-self.start_time > self.time_limit):  # Over time?
            raise SystemExit()  # Terminate thread.
        return self.localtrace

class best_value:
   def __init__(self):
      self.value = None

class OthelloGame:
    def __init__(self):
        self.board = [['.' for _ in range(COLS)] for _ in range(ROWS)]
        self.board[3][3] = self.board[4][4] = 'o'
        self.board[3][4] = self.board[4][3] = 'x'
        self.current_player = 'x'
        self.strategy = Strategy()
        self.best_move = None
        self.running = True
        self.turn_complete = False
        self.best_move = best_value()
        self.stop_thread = threading.Event()  # Event to signal thread to stop
        self.running = True  # Initialize running attribute

    def draw_board(self, screen):
        screen.fill(GREEN)
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.board[row][col] == 'x':
                    pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE // 3)
                elif self.board[row][col] == 'o':
                    pygame.draw.circle(screen, WHITE, rect.center, CELL_SIZE // 3)
                elif self.is_valid_move(row, col):
                    if self.current_player == 'x':
                        pygame.draw.circle(screen, BLUE, rect.center, CELL_SIZE // 6)
                    else:
                        pygame.draw.circle(screen, YELLOW, rect.center, CELL_SIZE // 6)
                pygame.draw.rect(screen, BLACK, rect, 1)

    def get_click_pos(self, mouse_pos):
        col = mouse_pos[0] // CELL_SIZE
        row = mouse_pos[1] // CELL_SIZE
        return row, col

    def flip_tokens(self, row, col, dr, dc):
        opponent = 'o' if self.current_player == 'x' else 'x'
        rowc= row+0
        colc= col+0
        drc= dr+0
        dcc= dc+0
        while 0 <= rowc < ROWS and 0 <= colc < COLS and self.board[rowc][colc] == opponent:
            rowc += drc
            colc += dcc
        if 0 <= rowc < ROWS and 0 <= colc < COLS and self.board[rowc][colc] == self.current_player:
            while 0 <= row < ROWS and 0 <= col < COLS and self.board[row][col] == opponent:
                self.board[row][col] = self.current_player
                row += dr
                col += dc

    def is_valid_move(self, row, col):
        if self.board[row][col] != '.':
            return False
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < ROWS and 0 <= c < COLS and self.board[r][c] != '.' and self.board[r][c] != self.current_player:
                while 0 <= r < ROWS and 0 <= c < COLS and self.board[r][c] != '.' and self.board[r][c] != self.current_player:
                    r += dr
                    c += dc
                if 0 <= r < ROWS and 0 <= c < COLS and self.board[r][c] == self.current_player:
                    return True
        return False

    def make_move(self, row, col):
        if self.is_valid_move(row, col):
            self.board[row][col] = self.current_player
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]
            for dr, dc in directions:
                self.flip_tokens(row + dr, col + dc, dr, dc)
            self.current_player = 'o' if self.current_player == 'x' else 'x'

    def check_winner(self):
        x_count = sum(row.count('x') for row in self.board)
        o_count = sum(row.count('o') for row in self.board)
        if x_count > o_count:
            return 'x'
        elif o_count > x_count:
            return 'o'
        else:
            return 'Draw'


    def ai_move_thread(self):
        self.strategy.best_strategy(''.join(''.join(self.board[i]) for i in range(COLS)), self.current_player, self.best_move, self.running, 5)

            
    def run(self):
        game_end = 0
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Othello Game')

        while self.running:
            # if len([self.is_valid_move(row, col) for row in range(ROWS) for col in range(COLS)])==0:
            #         print("NO MOves")
            #         break
            for event in pygame.event.get():
                # print(event.type)
                # print(event.type == QUIT)
                l =[]
                for row in range(ROWS):
                    for col in range(COLS):
                        if self.is_valid_move(row, col):
                            l.append((row, col))
                if len(l)==0:
                    print("No Moves for Human")
                    game_end +=1
                    self.turn_complete = True
                    self.current_player = 'o' if self.current_player == 'x' else 'x'
                    break
                else:
                    if game_end == 1:
                        game_end = 0
                if event.type == QUIT:
                    self.running = False
                elif event.type == MOUSEBUTTONDOWN and not self.turn_complete:
                    mouse_pos = pygame.mouse.get_pos()
                    row, col = self.get_click_pos(mouse_pos)
                    if 0 <= row < ROWS and 0 <= col < COLS and self.board[row][col] == '.' and self.is_valid_move(row, col):
                        self.make_move(row, col)
                        self.turn_complete = True
                        print(f'Player move: {row}, {col}')
                    else: continue
            self.draw_board(screen)
            pygame.display.flip()
            if len([self.is_valid_move(row, col) for row in range(ROWS) for col in range(COLS)])==0:
                winner = self.check_winner()
            # if winner != 'Draw':
                print(f"Winner: {winner}")
                self.running = False
            # AI's turn
            if self.current_player == 'o' and self.turn_complete:
                l =[]
                for row in range(ROWS):
                    for col in range(COLS):
                        if self.is_valid_move(row, col):
                            l.append((row, col))
                if len(l)==0:
                    print("No Moves for AI")
                    game_end +=1
                    if game_end > 1:
                        print("Game Over")
                        print(f"Winner: {self.check_winner()}")
                        self.running = False
                        continue
                    self.turn_complete = False
                    self.current_player = 'o' if self.current_player == 'x' else 'x'
                    continue
                else:
                    if game_end == 1:
                        game_end = 0
                self.best_move = best_value()
                

                # Run AI move in a separate thread with time limit
                ai_thread = StoppableThread(target=self.ai_move_thread, time_limit=TIME_LIMIT)
                ai_thread.start()
                ai_thread.join()  # Timeout after 5 seconds
                
                if ai_thread.is_alive():  # AI thread is still running after timeout
                    print("AI move timed out")
                    ai_thread.stop()

#                     self.stop_thread.set()  # Set the stop_thread flag to stop the AI thread
                    
                print(f'Best Value: {self.best_move.value}')
                if self.best_move.value is not None:
                    self.make_move(self.best_move.value // COLS, self.best_move.value % COLS)
                self.turn_complete = False
                self.draw_board(screen)
                pygame.display.flip()
            if len([self.is_valid_move(row, col) for row in range(ROWS) for col in range(COLS)])==0:
                winner = self.check_winner()
            # if winner != 'Draw':
                print(f"Winner: {winner}")
                self.running = False

        pygame.quit()
        
if __name__ == '__main__':
    game = OthelloGame()
    game.run()
