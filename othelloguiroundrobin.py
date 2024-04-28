from othellogui_copy2 import OthelloGame

players = ['OthelloRANDOM', 'OthelloMCTS1']

def run_game(agents, time_limit1=10, time_limit12=10):
    game = OthelloGame(agents, time_limit=time_limit1, time_limit2=time_limit12)
    game.run()
    if game.check_winner() == 'x':
        return [1, game.score2]
    else:
        return [0, game.score1]
    
def generate_roundRobinMatchings(players):
    return [(players[i], players[j]) for i in range(len(players)) for j in range(i+1, len(players))]

def run_roundRobin(players):
    matchings = generate_roundRobinMatchings(players)
    scores = {player: 0 for player in players}
    avg_poss = {player: 0 for player in players}
    for player1, player2 in matchings:
        g1 = run_game([player1, player2])
        g2 = run_game([player2, player1])
        if g1[0] == 1:
            scores[player2] += 1
            avg_poss[player2] += g1[1]/(len(players)/((len(players)-1)/2))
            avg_poss[player1] -= g1[1]/(len(players)/((len(players)-1)/2))
        else:
            scores[player1] += 1
            avg_poss[player2] -= g1[1]/(len(players)/((len(players)-1)/2))
            avg_poss[player1] += g1[1]/(len(players)/((len(players)-1)/2))
        if g2[0] == 1:
            scores[player1] += 1
            avg_poss[player1] += g2[1]/(len(players)/((len(players)-1)/2))
            avg_poss[player2] -= g2[1]/(len(players)/((len(players)-1)/2))
        else:
            scores[player2] += 1
            avg_poss[player1] -= g2[1]/(len(players)/((len(players)-1)/2))
            avg_poss[player2] += g2[1]/(len(players)/((len(players)-1)/2))
    return [scores, avg_poss]

def run_roundRobinNtimes(players, n):
    scores = {player: 0 for player in players}
    avg_poss = {player: 0 for player in players}
    for i in range(n):
        o = run_roundRobin(players)
        scores_i = o[0]
        poss_i = o[1]
        for player in players:
            scores[player] += scores_i[player]
            avg_poss[player] += poss_i[player]/n
    return [scores, avg_poss]

def print_rankings(scores):
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for player, score in sorted_scores:
        print(f'{player}: {score}')

def print_avg_poss(avg_poss):
    sorted_avg_poss = sorted(avg_poss.items(), key=lambda x: x[1], reverse=True)
    for player, avg_pos in sorted_avg_poss:
        print(f'{player}: {avg_pos}')

s = run_roundRobinNtimes(players, 3)
scores = s[0]
avg_poss = s[1]
print(f'\n\n\nWIN RANKINGS:\n______________________\n')
print_rankings(scores)
print(f'\n\nAVERAGE POSSESSIONS:\n______________________\n')
print_avg_poss(avg_poss)