import random
b2p = dict()


def possiblemoves(board, turn):
   if (''.join(board),turn) in b2p.keys():return b2p[(''.join(board),turn)]
   opponent = ['x','o'][turn=='x'];pmoves = set()
   for i in range(0,64,8):
      temp = 0
      for j in range(i,i+8):#left to right
         if board[j]==turn and not temp and j<i+7 and board[j+1] == opponent:temp=1
         elif board[j]==turn and temp and j<i+7 and not board[j+1] == opponent:temp=0
         if board[j]=='.' and temp:
            pmoves.add(j)
            temp=0
      temp=0
      for j in range(i+7,i-1,-1):#right to left
         if board[j]==turn and not temp and j>i and board[j-1] == opponent:temp=1
         if board[j]==turn and temp and j>i and not board[j-1] == opponent:temp=0
         if board[j]=='.' and temp:
            pmoves.add(j)
            temp=0
      temp=0
   for i in range(8):#top to down
      temp = 0
      for j in range(i,64,8):
         if board[j]==turn and not temp and j+8<64 and board[j+8] == opponent:temp=1
         elif board[j]==turn and temp and j+8<64 and not board[j+8] == opponent:temp=0
         if board[j]=='.' and temp:
            pmoves.add(j)
            temp=0
      temp=0
      for j in range(63-i,-1,-8):#down to up
         if board[j]==turn and not temp and j-8>=0 and board[j-8] == opponent:temp=1
         elif board[j]==turn and temp and j-8>=0 and not board[j-8] == opponent:temp=0
         if board[j]=='.' and temp:
            pmoves.add(j)
            temp=0
      temp=0
   turnindx = [idx for idx in range(len(board)) if board[idx]==turn]
   for idx in turnindx:
      col = idx%8
      if col+1>7 or idx+9>63 or not board[idx+9]==opponent:continue
      for i in range(idx+9,64,9):
         if i%8<col:break
         if board[i]==turn:break
         elif board[i]=='.':
            pmoves.add(i)
            break
   for idx in turnindx:
      col = idx%8
      if col-1<0 or idx-9<0 or not board[idx-9]==opponent:continue
      for i in range(idx-9,-1,-9):
         if i%8>col:break
         if board[i]==turn:break
         elif board[i]=='.':
            pmoves.add(i)
            break
   for idx in turnindx:
      col = idx%8
      if col-1<0 or idx+7>63 or not board[idx+7]==opponent:continue
      for i in range(idx+7,64,7):
         if i%8>=col:break
         if board[i]==turn:break
         elif board[i]=='.':
            pmoves.add(i)
            break
   for idx in turnindx:
      col = idx%8
      if col+1>7 or idx-7<0 or not board[idx-7]==opponent:continue
      for i in range(idx-7,0,-7):
         if i%8<col:break
         if board[i]==turn:break
         elif board[i]=='.':
            pmoves.add(i)
            break 
   b2p[(''.join(board),turn)]={*pmoves}
   return pmoves


class Strategy:
   logging=True
   def best_strategy(self, board, player, best_move, still_running, time_limit):
      best_move.value = random.choice(tuple(possiblemoves(board,player.lower())))
      return