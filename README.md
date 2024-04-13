Format for making an agent
Create a new python file and add its name to the respective import statement of GUI

```python
class Strategy:
  def best_strategy(self, board, player, best_move, still_running, time_limit):
    '''
    board: 64-character representation of a board e.g. board = '...........................ox......xo...........................'
    player: 'o' if white's turn, 'x' if black's turn
    best_move: set best_move.value to index you want to move to
    still_running: variable used for debugging for threading issues, dwai
    time_limit: time in seconds that the agent has to set best_move.value (thread will be killed after this time)
    '''
```
