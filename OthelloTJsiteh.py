import sys; args = sys.argv[1:]
# Akshan Sameullah, pd. 6
LIMIT_AB=12
GAMESINTOURNAMENT = 100
midgamedepth=2
import random
import time
b2p = dict()
b2m = dict()

def eval(tkn, eTkn, brd, pmoves, epmoves):
   tkncnt = brd.count(tkn)
   etkncnt = brd.count(eTkn)
   if tkncnt==0:
      return [-99999]
   return [(((-tkncnt/100)+len(pmoves)+(10*((brd[0]==tkn)+(brd[7]==tkn)+(brd[63]==tkn)+(brd[56]==tkn))))-((-etkncnt/100)+len(epmoves)+(10*((brd[0]==eTkn)+(brd[7]==eTkn)+(brd[63]==eTkn)+(brd[56]==eTkn)))))] # if tkn can't move


def showboard(board):
   for row in range(0,64,8):print(board[row:row+8])

def clearstars(board):
   o=[]
   for i in board:
      if not i=='*':o.append(i)
      else:o.append('.')
   return o
   
def makemove(board, move, turn):
   ob = ''.join(board)
   if (ob,move,turn) in b2m.keys():return b2m[(ob,move,turn)]
   move=int(move)
   opponent = ['x','o'][turn=='x']
   board[move] = turn[:]
   for i in range(move+1,move+(7-move%8)+1):
      if board[i]=='.':break
      if board[i]==turn:
         x=i-1
         while board[x]==opponent:
            board[x] = turn
            x-=1
         break
   for i in range(move-1,move-move%8-1,-1):
      if board[i]=='.':break
      if board[i]==turn:
         x=i+1
         while board[x]==opponent:
            board[x] = turn
            x+=1
         break
   for i in range(move+8,move+(7-move//8)*8+1,8):
      if board[i]=='.':break
      if board[i]==turn:
         x=i-8
         while board[x]==opponent:
            board[x] = turn
            x-=8
         break
   for i in range(move-8,-1,-8):
      if board[i]=='.':break
      if board[i]==turn:
         x=i+8
         while board[x]==opponent:
            board[x] = turn
            x+=8
         break
   col=move%8
   for i in range(move-9,-1,-9):
      if i%8>=col:break
      if board[i]=='.':break
      if board[i]==turn:
         x=i+9
         while board[x]==opponent:
            board[x] = turn
            x+=9
         break
   for i in range(move+9,64,9):
      if i%8<=col:break
      if board[i]=='.':break
      if board[i]==turn:
         x=i-9
         while board[x]==opponent:
            board[x] = turn
            x-=9
         break
   for i in range(move-7,-1,-7):
      if i%8<=col:break
      if board[i]=='.':break
      if board[i]==turn:
         x=i+7
         while board[x]==opponent:
            board[x] = turn
            x+=7
         break
   for i in range(move+7,64,7):
      if i%8>=col:break
      if board[i]=='.':break
      if board[i]==turn:
         x=i-7
         while board[x]==opponent:
            board[x] = turn
            x-=7
         break
   b2m[(ob,move,turn)]=''.join(board)
   return ''.join(board)

def processmove(move):
   if move[0].lower() in 'abcdefgh':move = (int(move[1])-1)*8+'abcdefgh'.find(move[0].lower())
   return move

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

def midgamealphabeta(brd, tkn, lowerBnd, upperBnd, depth, pre):
#  showboard(brd)
#  print(tkn, lowerBnd, upperBnd)
 eTkn = ['x','o'][tkn=='x']
 pmoves=possiblemoves(brd,tkn)
 epmoves=possiblemoves(brd,eTkn)
 if depth>=midgamedepth or (len(pmoves)==0 and len(epmoves)==0):
   return eval(tkn, eTkn, brd, pmoves, epmoves)
 if len(pmoves)==0 and len(epmoves): # if game is over
   ab=midgamealphabeta(brd, eTkn, -upperBnd, -lowerBnd, depth,pre)
   return [-ab[0]]+ab[1:]+[-1]
 best = [lowerBnd-1] # guarantees best will be set
 if pmoves&{0,7,56,63,pre+1,pre-1,pre+8,pre-8,pre-7,pre+7,pre-9,pre+9}:
   lpmoves=list(pmoves)
   for crnr in pmoves&{0,7,56,63,pre+1,pre-1,pre+8,pre-8,pre-7,pre+7,pre-9,pre+9}:
      lpmoves.remove(crnr)
   lpmoves = list(pmoves&{0,7,56,63,pre+1,pre-1,pre+8,pre-8,pre-7,pre+7,pre-9,pre+9})+lpmoves
   pmoves=lpmoves[:]
 for mv in pmoves:
   newBrd = makemove(list(brd),mv,tkn)
   ab = midgamealphabeta(newBrd, eTkn, -upperBnd, -lowerBnd, depth+1,mv)
   score = -ab[0] # Score from tkn's viewpt
   if score < lowerBnd: continue # Not an improvement
   if score > upperBnd: 
#       if score>63:print('score',score, ab, upperBnd)
      return [score] # Vile to the caller
   if score > best[0]:
      best=[-ab[0]] + ab[1:] + [mv] # Else it's an improvement
      lowerBnd = score+1
 return best


def midgamealphabetatop(brd, tkn, lowerBnd, upperBnd, best_move):
#  showboard(brd)
#  print(tkn, lowerBnd, upperBnd)
 eTkn = ['x','o'][tkn=='x']
 pmoves=possiblemoves(brd,tkn)
 epmoves=possiblemoves(brd,eTkn)
 if len(pmoves)==0 and len(epmoves)==0:
   tkncnt = brd.count(tkn)
   etkncnt = brd.count(eTkn)
   if tkncnt==0:return [-99999]
   return [(((tkncnt/100)+len(pmoves)+(10*((brd[0]==tkn)+(brd[7]==tkn)+(brd[63]==tkn)+(brd[56]==tkn))))-((etkncnt/100)+len(epmoves)+(10*((brd[0]==eTkn)+(brd[7]==eTkn)+(brd[63]==eTkn)+(brd[56]==eTkn)))))] # if tkn can't move
 if len(pmoves)==0 and len(epmoves): # if game is over
   ab=midgamealphabeta(brd, eTkn, -upperBnd, -lowerBnd, 0,0)
   return [-ab[0]]+ab[1:]+[-1]
 best = [lowerBnd-1] # guarantees best will be set
 if pmoves&{0,7,56,63}:
   lpmoves=list(pmoves)
   for crnr in pmoves&{0,7,56,63}:
      lpmoves.remove(crnr)
   lpmoves = list(pmoves&{0,7,56,63})+lpmoves
   pmoves=lpmoves[:]
 for mv in pmoves:
   newBrd = makemove(list(brd),mv,tkn)
#    print(mv)
#    showboard(newBrd)
   ab = midgamealphabeta(newBrd, eTkn, -upperBnd, -lowerBnd, 1,mv)
   score = -ab[0] # Score from tkn's viewpt
   if score < lowerBnd: continue # Not an improvement
   if score > upperBnd: return [score] # Vile to the caller
   if score > best[0]:
      best=[-ab[0]] + ab[1:] + [mv] # Else it's an improvement
      best_move.value = mv
      lowerBnd = score+1
 return best

def midgamealphabeta2(brd, tkn, lowerBnd, upperBnd, depth, pre):
#  showboard(brd)
#  print(tkn, lowerBnd, upperBnd)
 eTkn = ['x','o'][tkn=='x']
 pmoves=possiblemoves(brd,tkn)
 epmoves=possiblemoves(brd,eTkn)
 if depth>=(midgamedepth+1) or (len(pmoves)==0 and len(epmoves)==0):
   return eval(tkn, eTkn, brd, pmoves, epmoves)
 if len(pmoves)==0 and len(epmoves): # if game is over
   ab=midgamealphabeta2(brd, eTkn, -upperBnd, -lowerBnd, depth+1,pre)
   return [-ab[0]]+ab[1:]+[-1]
 best = [lowerBnd-1] # guarantees best will be set
 if pmoves&{0,7,56,63,pre+1,pre-1,pre+8,pre-8,pre-7,pre+7,pre-9,pre+9}:
   lpmoves=list(pmoves)
   for crnr in pmoves&{0,7,56,63,pre+1,pre-1,pre+8,pre-8,pre-7,pre+7,pre-9,pre+9}:
      lpmoves.remove(crnr)
   lpmoves = list(pmoves&{0,7,56,63,pre+1,pre-1,pre+8,pre-8,pre-7,pre+7,pre-9,pre+9})+lpmoves
   pmoves=lpmoves[:]
 for mv in pmoves:
   newBrd = makemove(list(brd),mv,tkn)
   ab = midgamealphabeta2(newBrd, eTkn, -upperBnd, -lowerBnd, depth+1,mv)
   score = -ab[0] # Score from tkn's viewpt
   if score < lowerBnd: continue # Not an improvement
   if score > upperBnd: 
#       if score>63:print('score',score, ab, upperBnd)
      return [score] # Vile to the caller
   if score > best[0]:
      best=[-ab[0]] + ab[1:] + [mv] # Else it's an improvement
      lowerBnd = score+1
 return best


def midgamealphabetatop2(brd, tkn, lowerBnd, upperBnd, best_move):
#  showboard(brd)
#  print(tkn, lowerBnd, upperBnd)
 eTkn = ['x','o'][tkn=='x']
 pmoves=possiblemoves(brd,tkn)
 epmoves=possiblemoves(brd,eTkn)
 if len(pmoves)==0 and len(epmoves)==0:
   tkncnt = brd.count(tkn)
   etkncnt = brd.count(eTkn)
   if tkncnt==0:return [-99999]
   return [(((tkncnt/100)+len(pmoves)+(10*((brd[0]==tkn)+(brd[7]==tkn)+(brd[63]==tkn)+(brd[56]==tkn))))-((etkncnt/100)+len(epmoves)+(10*((brd[0]==eTkn)+(brd[7]==eTkn)+(brd[63]==eTkn)+(brd[56]==eTkn)))))] # if tkn can't move
 if len(pmoves)==0 and len(epmoves): # if game is over
   ab=midgamealphabeta2(brd, eTkn, -upperBnd, -lowerBnd, 1,0)
   return [-ab[0]]+ab[1:]+[-1]
 best = [lowerBnd-1] # guarantees best will be set
 if pmoves&{0,7,56,63}:
   lpmoves=list(pmoves)
   for crnr in pmoves&{0,7,56,63}:
      lpmoves.remove(crnr)
   lpmoves = list(pmoves&{0,7,56,63})+lpmoves
   pmoves=lpmoves[:]
 for mv in pmoves:
   newBrd = makemove(list(brd),mv,tkn)
#    print(mv)
#    showboard(newBrd)
   ab = midgamealphabeta2(newBrd, eTkn, -upperBnd, -lowerBnd, 1,mv)
   score = -ab[0] # Score from tkn's viewpt
   if score < lowerBnd: continue # Not an improvement
   if score > upperBnd: return [score] # Vile to the caller
   if score > best[0]:
      best=[-ab[0]] + ab[1:] + [mv] # Else it's an improvement
      lowerBnd = score+1
 return best

def midgamealphabeta3(brd, tkn, lowerBnd, upperBnd, depth, pre):
#  showboard(brd)
#  print(tkn, lowerBnd, upperBnd)
 eTkn = ['x','o'][tkn=='x']
 pmoves=possiblemoves(brd,tkn)
 epmoves=possiblemoves(brd,eTkn)
 if depth>=(midgamedepth+2) or (len(pmoves)==0 and len(epmoves)==0):
   return eval(tkn, eTkn, brd, pmoves, epmoves)
 if len(pmoves)==0 and len(epmoves): # if game is over
   ab=midgamealphabeta3(brd, eTkn, -upperBnd, -lowerBnd, depth+1,pre)
   return [-ab[0]]+ab[1:]+[-1]
 best = [lowerBnd-1] # guarantees best will be set
 if pmoves&{0,7,56,63,pre+1,pre-1,pre+8,pre-8,pre-7,pre+7,pre-9,pre+9}:
   lpmoves=list(pmoves)
   for crnr in pmoves&{0,7,56,63,pre+1,pre-1,pre+8,pre-8,pre-7,pre+7,pre-9,pre+9}:
      lpmoves.remove(crnr)
   lpmoves = list(pmoves&{0,7,56,63,pre+1,pre-1,pre+8,pre-8,pre-7,pre+7,pre-9,pre+9})+lpmoves
   pmoves=lpmoves[:]
 for mv in pmoves:
   newBrd = makemove(list(brd),mv,tkn)
   ab = midgamealphabeta3(newBrd, eTkn, -upperBnd, -lowerBnd, depth+1,mv)
   score = -ab[0] # Score from tkn's viewpt
   if score < lowerBnd: continue # Not an improvement
   if score > upperBnd: 
#       if score>63:print('score',score, ab, upperBnd)
      return [score] # Vile to the caller
   if score > best[0]:
      best=[-ab[0]] + ab[1:] + [mv] # Else it's an improvement
      lowerBnd = score+1
 return best


def midgamealphabetatop3(brd, tkn, lowerBnd, upperBnd, best_move):
#  showboard(brd)
#  print(tkn, lowerBnd, upperBnd)
 eTkn = ['x','o'][tkn=='x']
 pmoves=possiblemoves(brd,tkn)
 epmoves=possiblemoves(brd,eTkn)
 if len(pmoves)==0 and len(epmoves)==0:
   tkncnt = brd.count(tkn)
   etkncnt = brd.count(eTkn)
   if tkncnt==0:return [-99999]
   return [(((tkncnt/100)+len(pmoves)+(10*((brd[0]==tkn)+(brd[7]==tkn)+(brd[63]==tkn)+(brd[56]==tkn))))-((etkncnt/100)+len(epmoves)+(10*((brd[0]==eTkn)+(brd[7]==eTkn)+(brd[63]==eTkn)+(brd[56]==eTkn)))))] # if tkn can't move
 if len(pmoves)==0 and len(epmoves): # if game is over
   ab=midgamealphabeta3(brd, eTkn, -upperBnd, -lowerBnd, 1,0)
   return [-ab[0]]+ab[1:]+[-1]
 best = [lowerBnd-1] # guarantees best will be set
 if pmoves&{0,7,56,63}:
   lpmoves=list(pmoves)
   for crnr in pmoves&{0,7,56,63}:
      lpmoves.remove(crnr)
   lpmoves = list(pmoves&{0,7,56,63})+lpmoves
   pmoves=lpmoves[:]
 for mv in pmoves:
   newBrd = makemove(list(brd),mv,tkn)
#    print(mv)
#    showboard(newBrd)
   ab = midgamealphabeta3(newBrd, eTkn, -upperBnd, -lowerBnd, 1,mv)
   score = -ab[0] # Score from tkn's viewpt
   if score < lowerBnd: continue # Not an improvement
   if score > upperBnd: return [score] # Vile to the caller
   if score > best[0]:
      best=[-ab[0]] + ab[1:] + [mv] # Else it's an improvement
      lowerBnd = score+1
 return best

def midgamealphabeta4(brd, tkn, lowerBnd, upperBnd, depth, pre):
#  showboard(brd)
#  print(tkn, lowerBnd, upperBnd)
 eTkn = ['x','o'][tkn=='x']
 pmoves=possiblemoves(brd,tkn)
 epmoves=possiblemoves(brd,eTkn)
 if depth>=(midgamedepth+3) or (len(pmoves)==0 and len(epmoves)==0):
   return eval(tkn, eTkn, brd, pmoves, epmoves)
 if len(pmoves)==0 and len(epmoves): # if game is over
   ab=midgamealphabeta4(brd, eTkn, -upperBnd, -lowerBnd, depth+1,pre)
   return [-ab[0]]+ab[1:]+[-1]
 best = [lowerBnd-1] # guarantees best will be set
 if pmoves&{0,7,56,63,pre+1,pre-1,pre+8,pre-8,pre-7,pre+7,pre-9,pre+9}:
   lpmoves=list(pmoves)
   for crnr in pmoves&{0,7,56,63,pre+1,pre-1,pre+8,pre-8,pre-7,pre+7,pre-9,pre+9}:
      lpmoves.remove(crnr)
   lpmoves = list(pmoves&{0,7,56,63,pre+1,pre-1,pre+8,pre-8,pre-7,pre+7,pre-9,pre+9})+lpmoves
   pmoves=lpmoves[:]
 for mv in pmoves:
   newBrd = makemove(list(brd),mv,tkn)
   ab = midgamealphabeta4(newBrd, eTkn, -upperBnd, -lowerBnd, depth+1,mv)
   score = -ab[0] # Score from tkn's viewpt
   if score < lowerBnd: continue # Not an improvement
   if score > upperBnd: 
#       if score>63:print('score',score, ab, upperBnd)
      return [score] # Vile to the caller
   if score > best[0]:
      best=[-ab[0]] + ab[1:] + [mv] # Else it's an improvement
      lowerBnd = score+1
 return best


def midgamealphabetatop4(brd, tkn, lowerBnd, upperBnd, best_move):
#  showboard(brd)
#  print(tkn, lowerBnd, upperBnd)
 eTkn = ['x','o'][tkn=='x']
 pmoves=possiblemoves(brd,tkn)
 epmoves=possiblemoves(brd,eTkn)
 if len(pmoves)==0 and len(epmoves)==0:
   tkncnt = brd.count(tkn)
   etkncnt = brd.count(eTkn)
   if tkncnt==0:return [-99999]
   return [(((tkncnt/100)+len(pmoves)+(10*((brd[0]==tkn)+(brd[7]==tkn)+(brd[63]==tkn)+(brd[56]==tkn))))-((etkncnt/100)+len(epmoves)+(10*((brd[0]==eTkn)+(brd[7]==eTkn)+(brd[63]==eTkn)+(brd[56]==eTkn)))))] # if tkn can't move
 if len(pmoves)==0 and len(epmoves): # if game is over
   ab=midgamealphabeta4(brd, eTkn, -upperBnd, -lowerBnd, 1,0)
   return [-ab[0]]+ab[1:]+[-1]
 best = [lowerBnd-1] # guarantees best will be set
 if pmoves&{0,7,56,63}:
   lpmoves=list(pmoves)
   for crnr in pmoves&{0,7,56,63}:
      lpmoves.remove(crnr)
   lpmoves = list(pmoves&{0,7,56,63})+lpmoves
   pmoves=lpmoves[:]
 for mv in pmoves:
   newBrd = makemove(list(brd),mv,tkn)
#    print(mv)
#    showboard(newBrd)
   ab = midgamealphabeta4(newBrd, eTkn, -upperBnd, -lowerBnd, 1,mv)
   score = -ab[0] # Score from tkn's viewpt
   if score < lowerBnd: continue # Not an improvement
   if score > upperBnd: return [score] # Vile to the caller
   if score > best[0]:
      best=[-ab[0]] + ab[1:] + [mv] # Else it's an improvement
      lowerBnd = score+1
 return best

def midgamealphabeta5(brd, tkn, lowerBnd, upperBnd, depth, pre):
#  showboard(brd)
#  print(tkn, lowerBnd, upperBnd)
 eTkn = ['x','o'][tkn=='x']
 pmoves=possiblemoves(brd,tkn)
 epmoves=possiblemoves(brd,eTkn)
 if depth>=(midgamedepth+4) or (len(pmoves)==0 and len(epmoves)==0):
   return eval(tkn, eTkn, brd, pmoves, epmoves)
 if len(pmoves)==0 and len(epmoves): # if game is over
   ab=midgamealphabeta5(brd, eTkn, -upperBnd, -lowerBnd, depth+1,pre)
   return [-ab[0]]+ab[1:]+[-1]
 best = [lowerBnd-1] # guarantees best will be set
 if pmoves&{0,7,56,63,pre+1,pre-1,pre+8,pre-8,pre-7,pre+7,pre-9,pre+9}:
   lpmoves=list(pmoves)
   for crnr in pmoves&{0,7,56,63,pre+1,pre-1,pre+8,pre-8,pre-7,pre+7,pre-9,pre+9}:
      lpmoves.remove(crnr)
   lpmoves = list(pmoves&{0,7,56,63,pre+1,pre-1,pre+8,pre-8,pre-7,pre+7,pre-9,pre+9})+lpmoves
   pmoves=lpmoves[:]
 for mv in pmoves:
   newBrd = makemove(list(brd),mv,tkn)
   ab = midgamealphabeta5(newBrd, eTkn, -upperBnd, -lowerBnd, depth+1,mv)
   score = -ab[0] # Score from tkn's viewpt
   if score < lowerBnd: continue # Not an improvement
   if score > upperBnd: 
#       if score>63:print('score',score, ab, upperBnd)
      return [score] # Vile to the caller
   if score > best[0]:
      best=[-ab[0]] + ab[1:] + [mv] # Else it's an improvement
      lowerBnd = score+1
 return best


def midgamealphabetatop5(brd, tkn, lowerBnd, upperBnd, best_move):
#  showboard(brd)
#  print(tkn, lowerBnd, upperBnd)
 eTkn = ['x','o'][tkn=='x']
 pmoves=possiblemoves(brd,tkn)
 epmoves=possiblemoves(brd,eTkn)
 if len(pmoves)==0 and len(epmoves)==0:
   tkncnt = brd.count(tkn)
   etkncnt = brd.count(eTkn)
   if tkncnt==0:return [-99999]
   return [(((tkncnt/100)+len(pmoves)+(10*((brd[0]==tkn)+(brd[7]==tkn)+(brd[63]==tkn)+(brd[56]==tkn))))-((etkncnt/100)+len(epmoves)+(10*((brd[0]==eTkn)+(brd[7]==eTkn)+(brd[63]==eTkn)+(brd[56]==eTkn)))))] # if tkn can't move
 if len(pmoves)==0 and len(epmoves): # if game is over
   ab=midgamealphabeta5(brd, eTkn, -upperBnd, -lowerBnd, 1,0)
   return [-ab[0]]+ab[1:]+[-1]
 best = [lowerBnd-1] # guarantees best will be set
 if pmoves&{0,7,56,63}:
   lpmoves=list(pmoves)
   for crnr in pmoves&{0,7,56,63}:
      lpmoves.remove(crnr)
   lpmoves = list(pmoves&{0,7,56,63})+lpmoves
   pmoves=lpmoves[:]
 for mv in pmoves:
   newBrd = makemove(list(brd),mv,tkn)
#    print(mv)
#    showboard(newBrd)
   ab = midgamealphabeta5(newBrd, eTkn, -upperBnd, -lowerBnd, 1,mv)
   score = -ab[0] # Score from tkn's viewpt
   if score < lowerBnd: continue # Not an improvement
   if score > upperBnd: return [score] # Vile to the caller
   if score > best[0]:
      best=[-ab[0]] + ab[1:] + [mv] # Else it's an improvement
      lowerBnd = score+1
 return best

def midgamealphabeta6(brd, tkn, lowerBnd, upperBnd, depth, pre):
#  showboard(brd)
#  print(tkn, lowerBnd, upperBnd)
 eTkn = ['x','o'][tkn=='x']
 pmoves=possiblemoves(brd,tkn)
 epmoves=possiblemoves(brd,eTkn)
 if depth>=(midgamedepth+5) or (len(pmoves)==0 and len(epmoves)==0):
   return eval(tkn, eTkn, brd, pmoves, epmoves)
 if len(pmoves)==0 and len(epmoves): # if game is over
   ab=midgamealphabeta6(brd, eTkn, -upperBnd, -lowerBnd, depth+1,pre)
   return [-ab[0]]+ab[1:]+[-1]
 best = [lowerBnd-1] # guarantees best will be set
 if pmoves&{0,7,56,63,pre+1,pre-1,pre+8,pre-8,pre-7,pre+7,pre-9,pre+9}:
   lpmoves=list(pmoves)
   for crnr in pmoves&{0,7,56,63,pre+1,pre-1,pre+8,pre-8,pre-7,pre+7,pre-9,pre+9}:
      lpmoves.remove(crnr)
   lpmoves = list(pmoves&{0,7,56,63,pre+1,pre-1,pre+8,pre-8,pre-7,pre+7,pre-9,pre+9})+lpmoves
   pmoves=lpmoves[:]
 for mv in pmoves:
   newBrd = makemove(list(brd),mv,tkn)
   ab = midgamealphabeta6(newBrd, eTkn, -upperBnd, -lowerBnd, depth+1,mv)
   score = -ab[0] # Score from tkn's viewpt
   if score < lowerBnd: continue # Not an improvement
   if score > upperBnd: 
#       if score>63:print('score',score, ab, upperBnd)
      return [score] # Vile to the caller
   if score > best[0]:
      best=[-ab[0]] + ab[1:] + [mv] # Else it's an improvement
      lowerBnd = score+1
 return best


def midgamealphabetatop6(brd, tkn, lowerBnd, upperBnd, best_move):
#  showboard(brd)
#  print(tkn, lowerBnd, upperBnd)
 eTkn = ['x','o'][tkn=='x']
 pmoves=possiblemoves(brd,tkn)
 epmoves=possiblemoves(brd,eTkn)
 if len(pmoves)==0 and len(epmoves)==0:
   tkncnt = brd.count(tkn)
   etkncnt = brd.count(eTkn)
   if tkncnt==0:return [-99999]
   return [(((tkncnt/100)+len(pmoves)+(10*((brd[0]==tkn)+(brd[7]==tkn)+(brd[63]==tkn)+(brd[56]==tkn))))-((etkncnt/100)+len(epmoves)+(10*((brd[0]==eTkn)+(brd[7]==eTkn)+(brd[63]==eTkn)+(brd[56]==eTkn)))))] # if tkn can't move
 if len(pmoves)==0 and len(epmoves): # if game is over
   ab=midgamealphabeta6(brd, eTkn, -upperBnd, -lowerBnd, 1,0)
   return [-ab[0]]+ab[1:]+[-1]
 best = [lowerBnd-1] # guarantees best will be set
 if pmoves&{0,7,56,63}:
   lpmoves=list(pmoves)
   for crnr in pmoves&{0,7,56,63}:
      lpmoves.remove(crnr)
   lpmoves = list(pmoves&{0,7,56,63})+lpmoves
   pmoves=lpmoves[:]
 for mv in pmoves:
   newBrd = makemove(list(brd),mv,tkn)
#    print(mv)
#    showboard(newBrd)
   ab = midgamealphabeta6(newBrd, eTkn, -upperBnd, -lowerBnd, 1,mv)
   score = -ab[0] # Score from tkn's viewpt
   if score < lowerBnd: continue # Not an improvement
   if score > upperBnd: return [score] # Vile to the caller
   if score > best[0]:
      best=[-ab[0]] + ab[1:] + [mv] # Else it's an improvement
      lowerBnd = score+1
 return best

def midgamealphabeta7(brd, tkn, lowerBnd, upperBnd, depth, pre):
#  showboard(brd)
#  print(tkn, lowerBnd, upperBnd)
 eTkn = ['x','o'][tkn=='x']
 pmoves=possiblemoves(brd,tkn)
 epmoves=possiblemoves(brd,eTkn)
 if depth>=(midgamedepth+6) or (len(pmoves)==0 and len(epmoves)==0):
   return eval(tkn, eTkn, brd, pmoves, epmoves)
 if len(pmoves)==0 and len(epmoves): # if game is over
   ab=midgamealphabeta7(brd, eTkn, -upperBnd, -lowerBnd, depth+1,pre)
   return [-ab[0]]+ab[1:]+[-1]
 best = [lowerBnd-1] # guarantees best will be set
 if pmoves&{0,7,56,63,pre+1,pre-1,pre+8,pre-8,pre-7,pre+7,pre-9,pre+9}:
   lpmoves=list(pmoves)
   for crnr in pmoves&{0,7,56,63,pre+1,pre-1,pre+8,pre-8,pre-7,pre+7,pre-9,pre+9}:
      lpmoves.remove(crnr)
   lpmoves = list(pmoves&{0,7,56,63,pre+1,pre-1,pre+8,pre-8,pre-7,pre+7,pre-9,pre+9})+lpmoves
   pmoves=lpmoves[:]
 for mv in pmoves:
   newBrd = makemove(list(brd),mv,tkn)
   ab = midgamealphabeta7(newBrd, eTkn, -upperBnd, -lowerBnd, depth+1,mv)
   score = -ab[0] # Score from tkn's viewpt
   if score < lowerBnd: continue # Not an improvement
   if score > upperBnd: 
#       if score>63:print('score',score, ab, upperBnd)
      return [score] # Vile to the caller
   if score > best[0]:
      best=[-ab[0]] + ab[1:] + [mv] # Else it's an improvement
      lowerBnd = score+1
 return best


def midgamealphabetatop7(brd, tkn, lowerBnd, upperBnd, best_move):
#  showboard(brd)
#  print(tkn, lowerBnd, upperBnd)
 eTkn = ['x','o'][tkn=='x']
 pmoves=possiblemoves(brd,tkn)
 epmoves=possiblemoves(brd,eTkn)
 if len(pmoves)==0 and len(epmoves)==0:
   tkncnt = brd.count(tkn)
   etkncnt = brd.count(eTkn)
   if tkncnt==0:return [-99999]
   return [(((tkncnt/100)+len(pmoves)+(10*((brd[0]==tkn)+(brd[7]==tkn)+(brd[63]==tkn)+(brd[56]==tkn))))-((etkncnt/100)+len(epmoves)+(10*((brd[0]==eTkn)+(brd[7]==eTkn)+(brd[63]==eTkn)+(brd[56]==eTkn)))))] # if tkn can't move
 if len(pmoves)==0 and len(epmoves): # if game is over
   ab=midgamealphabeta7(brd, eTkn, -upperBnd, -lowerBnd, 1,0)
   return [-ab[0]]+ab[1:]+[-1]
 best = [lowerBnd-1] # guarantees best will be set
 if pmoves&{0,7,56,63}:
   lpmoves=list(pmoves)
   for crnr in pmoves&{0,7,56,63}:
      lpmoves.remove(crnr)
   lpmoves = list(pmoves&{0,7,56,63})+lpmoves
   pmoves=lpmoves[:]
 for mv in pmoves:
   newBrd = makemove(list(brd),mv,tkn)
#    print(mv)
#    showboard(newBrd)
   ab = midgamealphabeta7(newBrd, eTkn, -upperBnd, -lowerBnd, 1,mv)
   score = -ab[0] # Score from tkn's viewpt
   if score < lowerBnd: continue # Not an improvement
   if score > upperBnd: return [score] # Vile to the caller
   if score > best[0]:
      best=[-ab[0]] + ab[1:] + [mv] # Else it's an improvement
      lowerBnd = score+1
 return best

def midgamealphabeta8(brd, tkn, lowerBnd, upperBnd, depth, pre):
#  showboard(brd)
#  print(tkn, lowerBnd, upperBnd)
 eTkn = ['x','o'][tkn=='x']
 pmoves=possiblemoves(brd,tkn)
 epmoves=possiblemoves(brd,eTkn)
 if depth>=(midgamedepth+7) or (len(pmoves)==0 and len(epmoves)==0):
   return eval(tkn, eTkn, brd, pmoves, epmoves)
 if len(pmoves)==0 and len(epmoves): # if game is over
   ab=midgamealphabeta8(brd, eTkn, -upperBnd, -lowerBnd, depth+1,pre)
   return [-ab[0]]+ab[1:]+[-1]
 best = [lowerBnd-1] # guarantees best will be set
 if pmoves&{0,7,56,63,pre+1,pre-1,pre+8,pre-8,pre-7,pre+7,pre-9,pre+9}:
   lpmoves=list(pmoves)
   for crnr in pmoves&{0,7,56,63,pre+1,pre-1,pre+8,pre-8,pre-7,pre+7,pre-9,pre+9}:
      lpmoves.remove(crnr)
   lpmoves = list(pmoves&{0,7,56,63,pre+1,pre-1,pre+8,pre-8,pre-7,pre+7,pre-9,pre+9})+lpmoves
   pmoves=lpmoves[:]
 for mv in pmoves:
   newBrd = makemove(list(brd),mv,tkn)
   ab = midgamealphabeta8(newBrd, eTkn, -upperBnd, -lowerBnd, depth+1,mv)
   score = -ab[0] # Score from tkn's viewpt
   if score < lowerBnd: continue # Not an improvement
   if score > upperBnd: 
#       if score>63:print('score',score, ab, upperBnd)
      return [score] # Vile to the caller
   if score > best[0]:
      best=[-ab[0]] + ab[1:] + [mv] # Else it's an improvement
      lowerBnd = score+1
 return best


def midgamealphabetatop8(brd, tkn, lowerBnd, upperBnd, best_move):
#  showboard(brd)
#  print(tkn, lowerBnd, upperBnd)
 eTkn = ['x','o'][tkn=='x']
 pmoves=possiblemoves(brd,tkn)
 epmoves=possiblemoves(brd,eTkn)
 if len(pmoves)==0 and len(epmoves)==0:
   tkncnt = brd.count(tkn)
   etkncnt = brd.count(eTkn)
   if tkncnt==0:return [-99999]
   return [(((tkncnt/100)+len(pmoves)+(10*((brd[0]==tkn)+(brd[7]==tkn)+(brd[63]==tkn)+(brd[56]==tkn))))-((etkncnt/100)+len(epmoves)+(10*((brd[0]==eTkn)+(brd[7]==eTkn)+(brd[63]==eTkn)+(brd[56]==eTkn)))))] # if tkn can't move
 if len(pmoves)==0 and len(epmoves): # if game is over
   ab=midgamealphabeta8(brd, eTkn, -upperBnd, -lowerBnd, 1,0)
   return [-ab[0]]+ab[1:]+[-1]
 best = [lowerBnd-1] # guarantees best will be set
 if pmoves&{0,7,56,63}:
   lpmoves=list(pmoves)
   for crnr in pmoves&{0,7,56,63}:
      lpmoves.remove(crnr)
   lpmoves = list(pmoves&{0,7,56,63})+lpmoves
   pmoves=lpmoves[:]
 for mv in pmoves:
   newBrd = makemove(list(brd),mv,tkn)
#    print(mv)
#    showboard(newBrd)
   ab = midgamealphabeta8(newBrd, eTkn, -upperBnd, -lowerBnd, 1,mv)
   score = -ab[0] # Score from tkn's viewpt
   if score < lowerBnd: continue # Not an improvement
   if score > upperBnd: return [score] # Vile to the caller
   if score > best[0]:
      best=[-ab[0]] + ab[1:] + [mv] # Else it's an improvement
      lowerBnd = score+1
 return best


def alphabeta(brd, tkn, lowerBnd, upperBnd):
 eTkn = ['x','o'][tkn=='x']
 pmoves=possiblemoves(brd,tkn)
 epmoves=possiblemoves(brd,eTkn)
 if len(pmoves)==0 and len(epmoves)==0:return [brd.count(tkn)-brd.count(eTkn)] # if tkn can't move
 if len(pmoves)==0 and len(epmoves): # if game is over
   ab=alphabeta(brd, eTkn, -upperBnd, -lowerBnd)
   return [-ab[0]]+ab[1:]+[-1]
 best = [lowerBnd-1] # guarantees best will be set
 if pmoves&{0,7,56,63}:
   lpmoves=list(pmoves)
   for crnr in pmoves&{0,7,56,63}:
      lpmoves.remove(crnr)
   lpmoves = list(pmoves&{0,7,56,63})+lpmoves
   pmoves=lpmoves[:]
 for mv in pmoves:
   newBrd = makemove(list(brd),mv,tkn)
   ab = alphabeta(newBrd, eTkn, -upperBnd, -lowerBnd)
   score = -ab[0] # Score from tkn's viewpt
   if score < lowerBnd: continue # Not an improvement
   if score > upperBnd: return [score] # Vile to the caller
   if score > best[0]:
      best=[-ab[0]] + ab[1:] + [mv] # Else it's an improvement
      lowerBnd = score+1
 return best
 
def alphabetatop(brd, tkn, lowerBnd, upperBnd, best_move):
 eTkn = ['x','o'][tkn=='x']
 pmoves=possiblemoves(brd,tkn)
 epmoves=possiblemoves(brd,eTkn)
 if len(pmoves)==0 and len(epmoves)==0:return [brd.count(tkn)-brd.count(eTkn)] # if tkn can't move
 if len(pmoves)==0 and len(epmoves): # if game is over
   ab=alphabeta(brd, eTkn, -upperBnd, -lowerBnd)
   return [-ab[0]]+ab[1:]+[-1]
 best = [lowerBnd-1] # guarantees best will be set
 if pmoves&{0,7,56,63}:
   lpmoves=list(pmoves)
   for crnr in pmoves&{0,7,56,63}:
      lpmoves.remove(crnr)
   lpmoves = list(pmoves&{0,7,56,63})+lpmoves
   pmoves=lpmoves[:]
 for mv in pmoves:
   newBrd = makemove(list(brd),mv,tkn)
   ab = alphabeta(newBrd, eTkn, -upperBnd, -lowerBnd)
   score = -ab[0] # Score from tkn's viewpt
   if score < lowerBnd: continue # Not an improvement
   if score > upperBnd: return [score] # Vile to the caller
   if score > best[0]:
      best=[-ab[0]] + ab[1:] + [mv] # Else it's an improvement
      best_move.value = mv
      lowerBnd = score+1
 return best
 
def go(input):
   if len(input)>0:
      if len(input[0])==64:
         board = list(input[0].lower())
         if len(input)>1:
            if input[1] in 'xXoO':
               turn = input[1].lower()
               if len(input)>2:moves = input[2:]
               else:moves = []
            else: 
               if not (board.count('x')+board.count('o'))%2:turn = 'x'
               else:turn='o'
               moves = input[1:]
         else: 
            if not (board.count('x')+board.count('o'))%2:turn = 'x'
            else:turn='o'
            moves = []
      elif input[0] in 'xXoO':
         board=['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'o', 'x', '.', '.', '.', '.', '.', '.', 'x', 'o', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']
         turn = input[0].lower()
         moves = input[1:]
      else:
         board=['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'o', 'x', '.', '.', '.', '.', '.', '.', 'x', 'o', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']
         turn = 'x'
         moves = input[:]
   else:
      board=['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'o', 'x', '.', '.', '.', '.', '.', '.', 'x', 'o', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']
      turn = 'x'
      moves = []
   if turn =='x':opponent='o'
   else:opponent='x'
   pmoves= possiblemoves(board,turn)
   if len(pmoves)==0:
      turn = ['x','o'][turn=='x']
   pmoves= possiblemoves(board,turn)
   oldboard = board[:]
   board= list(board)
   for i in pmoves:board[i] = '*'
   board = ''.join(board)
   if len(pmoves)==0:return -1
   else:
      if oldboard.count('.')<LIMIT_AB:
         moveseq = alphabeta(clearstars(oldboard), turn, -65, 65)
         return moveseq[-1]
      moveseq=midgamealphabeta(clearstars(oldboard), turn, -100000, 100000,0)
      if moveseq[-1]>63:print(moveseq)
      return moveseq[-1]
   print('')
   for idx in range(len(moves)):
      board=clearstars(board)
      if len(moves)>0:
         pmoves= possiblemoves(board,turn)
         if len(pmoves)==0:turn = ['x','o'][turn=='x']
         if len(moves)>0:
            if not (int(processmove(moves[idx])) in possiblemoves(board,turn)):continue
            moves[idx] = processmove(moves[idx])
            board=makemove(list(board), moves[idx], turn)
         turn = ['x','o'][turn=='x']
         pmoves= possiblemoves(board,turn)
         oldboard = board[:]
         board= list(board)
         for i in pmoves:board[i] = '*'
         board = ''.join(board)
      showboard(board)
      print('')
      print(oldboard,str(board.count('x'))+'/'+str(board.count('o')))
      if len(pmoves)==0:print('No moves possible')
      else:
         print(f'Possible moves for {turn}:', ', '.join([str(idx) for idx in pmoves]))
      print('')
   turn = ['x','o'][turn=='x']
   if len(pmoves)==0 and len(possiblemoves(board,turn))>0:
      pmoves= possiblemoves(board,turn)
      oldboard = board[:]
      board= list(board)
      for i in pmoves:
         board[i] = '*'
      board = ''.join(board)
      showboard(board)
      print('')
      print(oldboard,str(board.count('x'))+'/'+str(board.count('o')))
      if len(pmoves)==0:print('No moves possible')
      else:
         print(f'Possible moves for {turn}:', ', '.join([str(idx) for idx in pmoves]))
      print('')
      
def playGame(tkn):
  board = '...........................ox......xo...........................';enemyTkn = ['x','o'][tkn=='x'];turn  = 'x';moveseq=[]
  while len(possiblemoves(board,tkn))>0 or len(possiblemoves(board,enemyTkn))>0:
    move=0
    if tkn==turn:move=go([board,turn])
    else:
      if len(possiblemoves(board,turn))==0:move = -1
      else:move=random.choice(tuple(possiblemoves(board,turn)))
    
    board=makemove(list(board), move, turn);turn = ['x','o'][turn=='x'];moveseq.append(move)
  return [moveseq, board.count(tkn), 64-board.count('.'), tkn, board.count(enemyTkn)]

def runTournament(gameCnt):
  start = time.time();mytkncnt = 0;ttltkncnt = 0;lowesttkn = 'x';otherlowesttkn = 'x';lowestnum = -1;otherlowestnum = -1
  lowestscore = 65;lowestscoremoves = [];otherlowestscore = 65;otherlowestscoremoves = []
  for gameIdx in range(gameCnt):
    if not (gameIdx)%10:print()
    result = playGame('xo'[gameIdx % 2])
    print(' '*(((result[1]-result[4])>=0)+((result[1]-result[4])<10 and (result[1]-result[4])>-10))+str(result[1]-result[4]), end=' ', flush=True)
    mytkncnt+=result[1];ttltkncnt+=result[2]
    if result[1]-result[4]<lowestscore:
      if result[1]-result[4]<otherlowestscore:otherlowestscore = result[1]-result[4];otherlowestscoremoves = result[0];otherlowestnum = gameIdx+1;otherlowesttkn = result[3]
      else:lowestscore = result[1]-result[4];lowestscoremoves = result[0];lowestnum = gameIdx+1;lowesttkn = result[3]
  print(f'\nMy token count: {mytkncnt}');print(f'Total token count: {ttltkncnt}')
  print(f'Score so far {str(100*mytkncnt/ttltkncnt)[:str(100*mytkncnt/ttltkncnt).index(".")+2]}%')
  print(f'AB LIMIT: {LIMIT_AB}');print(f'Game {lowestnum} as {lowesttkn} => {lowestscore}: {" ".join(str(m) for m in lowestscoremoves)}')
  print(f'Game {otherlowestnum} as {otherlowesttkn} => {otherlowestscore}: {" ".join(str(m) for m in otherlowestscoremoves)}')
  print(f'Elapsed Time: {str(time.time()-start)[:str(time.time()-start).index(".")+2]}s')

def shapshot(board, move, turn):
   pmoves= possiblemoves(board,turn);oldboard = board[:];board=makemove(list(board), move, turn);board= list(board)
   for i in pmoves:board[i] = '*'
   board[move]=board[move].upper();print();board = ''.join(board);showboard(board);print()
   print(board.lower(),str(board.lower().count('x'))+'/'+str(board.lower().count('o')))
   print(f'Possible moves for {turn}:', ', '.join([str(idx) for idx in pmoves]))



class Strategy:
   logging=True
   def best_strategy(self, board, player, best_move, still_running, time_limit):
      input = [board, player]
      start = time.time()
      if len(input)>0:
         if len(input[0])==64:
            board = input[0].lower()
            if len(input)>1:
               if input[1] in 'xXoO':
                  turn = input[1].lower()
                  if len(input)>2:moves = input[2:]
                  else:moves = []
               else: 
                  if not (board.count('x')+board.count('o'))%2:turn = 'x'
                  else:turn='o'
                  moves = input[1:]
            else: 
               if not (board.count('x')+board.count('o'))%2:turn = 'x'
               else:turn='o'
               moves = []
         elif input[0] in 'xXoO':
            board='...........................ox......xo...........................';turn = input[0].lower();moves = input[1:]
         else:
            board='...........................ox......xo...........................';turn = 'x';moves = input[:]
      else:
         board='...........................ox......xo...........................';turn = 'x';moves = []
      best_move.value = random.choice(tuple(possiblemoves(board,turn)))
      opponent = ['x','o'][turn=='x'];pmoves= possiblemoves(board,turn)
      if len(pmoves)==0:turn = ['x','o'][turn=='x']
      pmoves= possiblemoves(board,turn);oldboard = board[:];board= list(board)
      board = ''.join(board)
   #    print(board)
   #    print(board=='...................x.......xx......xo...........................')
      if board=='..........................xxx......xo...........................' and turn== 'o':
       best_move.value= 20
       return
      if board=='...................x.......xx......xo...........................' and turn== 'o':
       best_move.value= 20
       return
      if board=='...........................ox......xx.......x...................' and turn== 'o':
       best_move.value=45
       return
      if board=='...........................ox......xxx..........................' and turn== 'o':
       best_move.value=45
       return
      if board=='..........................xxx.....ooo...........................' and turn== 'x':
       best_move.value=43
       return
      if board=='..................o.......xox......xo...........................' and turn== 'x':
       best_move.value=19
       return
      if board=='....................o.....xxo......xo...........................' and turn== 'x':
       best_move.value=29
       return
      if board=='...........................ox......xo...........................' and turn== 'x':
       best_move.value=19
       return
      if board=='...................x.......xx.....ooo...........................' and turn== 'x':
       best_move.value=45
       return
      if board=='..................ox.......ox......xo...........................' and turn== 'x':
       best_move.value=26
       return
      if board=='...................xo......xo......xo...........................' and turn== 'x':
       best_move.value=29
       return
      if board=='...........................ox......xo...........................' and turn=='x':
         best_move.value =19
         return
      if board=='..........................xxx......xo...........................':
         best_move.value =18
         return
      if board=='..................ox......xxx......xo...........................':
         best_move.value =34
         return
      if board=='..................o.......xox......xo...........................':
         best_move.value =19
         return
      if board=='..................ox......oxx.....ooo...........................':
         best_move.value =17
         return
      if board=='.................xxx......oxx.....ooo...........................':
         best_move.value =29
         return
      if board=='.................xxx......oooo....ooo...........................':
         best_move.value =33
         return
      if board=='.................xxx......xooo...xooo...........................':
         best_move.value =25
         return
      if board=='.................xxx.....ooooo...xooo...........................':
         best_move.value =42
         return
      if board=='.................xxx.....oxooo...xxoo.....x.....................':
         best_move.value =43
         return
      if board=='.................xxx.....oxooo...xooo.....xo....................':
         best_move.value =37
         return
      if board=='...................x.......xx......xo...........................':
         best_move.value =18
         return
      if board=='...........................ox......xx.......x...................':
         best_move.value =45
         return
      if board=='...........................ox......xxx..........................':
         best_move.value =45
         return
      if board=='...................x.......xx.....xoo....x......................':
         best_move.value =21
         return
      if board=='...................x.o.....xxx....xoo....x......................':
         best_move.value =20
         return
   
      board = list(board)
      for i in pmoves:board[i] = '*'
      board = ''.join(board);showboard(board);print('');print(oldboard,str(board.count('x'))+'/'+str(board.count('o')))
      if len(pmoves)==0:print('No moves possible')
      else:
         print(f'Possible moves for {turn}:', ', '.join([str(idx) for idx in pmoves]))
         if oldboard.count('.')<LIMIT_AB:
            moveseq = alphabetatop(clearstars(oldboard), turn, -65, 65, best_move);print(f'Min score: {moveseq[0]}; move sequence: {moveseq[1:]}');print( moveseq[-1])
            best_move.value = moveseq[-1]
         else:
            moveseq = midgamealphabetatop(clearstars(oldboard), turn, -100000, 100000, best_move);print( moveseq[-1])
            print('depth 2 reached')
            print(f'Elapsed Time: {str(time.time()-start)[:str(time.time()-start).index(".")+2]}s')
            best_move.value = moveseq[-1]
            moveseq = midgamealphabetatop2(clearstars(oldboard), turn, -100000, 100000, best_move);print( moveseq[-1])
            print('depth 3 reached')
            best_move.value = moveseq[-1]
            moveseq = midgamealphabetatop3(clearstars(oldboard), turn, -100000, 100000, best_move);print( moveseq[-1])
            print('depth 4 reached')
            best_move.value = moveseq[-1]
            moveseq = midgamealphabetatop4(clearstars(oldboard), turn, -100000, 100000, best_move);print( moveseq[-1])
            print('depth 5 reached')
            best_move.value = moveseq[-1]
            moveseq = midgamealphabetatop5(clearstars(oldboard), turn, -100000, 100000, best_move);print( moveseq[-1])
            print('depth 6 reached')
            best_move.value = moveseq[-1]
            moveseq = midgamealphabetatop6(clearstars(oldboard), turn, -100000, 100000, best_move);print( moveseq[-1])
            print('depth 7 reached')
            best_move.value = moveseq[-1]
            moveseq = midgamealphabetatop7(clearstars(oldboard), turn, -100000, 100000, best_move);print( moveseq[-1])
            print('depth 8 reached')
            best_move.value = moveseq[-1]
            moveseq = midgamealphabetatop8(clearstars(oldboard), turn, -100000, 100000, best_move);print( moveseq[-1])
            print('depth 9 reached')
            best_move.value = moveseq[-1]

         return moveseq[-1]
      print('')
      for idx in range(len(moves)):
         board=clearstars(board)
         if len(moves)>0:
            pmoves= possiblemoves(board,turn)
            if len(pmoves)==0:turn = ['x','o'][turn=='x']
            if len(moves)>0:
               if not (int(processmove(moves[idx])) in possiblemoves(board,turn)):continue
               moves[idx] = processmove(moves[idx])
               board=makemove(list(board), moves[idx], turn)
               print(f'{turn} moves to {moves[idx]}')
            turn = ['x','o'][turn=='x'];pmoves= possiblemoves(board,turn);oldboard = board[:];board= list(board)
            for i in pmoves:board[i] = '*'
            board = ''.join(board)
         showboard(board)
         print('')
         print(oldboard,str(board.count('x'))+'/'+str(board.count('o')))
         if len(pmoves)==0:print('No moves possible')
         else:print(f'Possible moves for {turn}:', ', '.join([str(idx) for idx in pmoves]))
         print('')
      turn = ['x','o'][turn=='x']
      if len(pmoves)==0 and len(possiblemoves(board,turn))>0:
         pmoves= possiblemoves(board,turn);oldboard = board[:];board= list(board)
         for i in pmoves:board[i] = '*'
         board = ''.join(board);showboard(board);print('');print(oldboard,str(board.count('x'))+'/'+str(board.count('o')))
         if len(pmoves)==0:print('No moves possible')
         else:print(f'Possible moves for {turn}:', ', '.join([str(idx) for idx in pmoves]))
         print('')
   
#    def main():
#      if not args: runTournament(GAMESINTOURNAMENT)
#      else: individualMoveProcessing(args)
#    
# if __name__ == '__main__': main()