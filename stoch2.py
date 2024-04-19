import matplotlib.pyplot as plt
import numpy as np


def winner_serves_match(pa, pb):
    player_serving = 'A'  # Player A serves first
    score_A = 0
    score_B = 0
    
    while (score_A < 5 and score_B < 5) or abs(score_A - score_B)<2:#the second condition here checks for deuce
        if player_serving == 'A':
            if not np.random.choice(2,1,p=[pa,1-pa])[0]: #we choose 0 with pa,
                score_A += 1 #score update
            else:
                score_B += 1
                player_serving = 'B' #swap for winner
        else:
            if not np.random.choice(2,1,p=[pb,1-pb])[0]: 
                score_A += 1
                player_serving = 'A'
            else:
                score_B += 1 #score update

        ret = 'A'
        if(score_B>score_A):
            ret='B'
        
        if(score_A>500):
            return ret
    return ret


def alternating_service_match(pa, pb):
    score_A = 0
    score_B = 0
    player_serving = 'A'  # Player A serves first
    
    while (score_A < 5 and score_B < 5) or abs(score_A-score_B)<2:
        if player_serving == 'A':
            if  not np.random.choice(2,1,p=[pa,1-pa])[0]:
                score_A += 1
            else:
                score_B += 1  #score update
        else:
            if  not np.random.choice(2,1,p=[pb,1-pb])[0]:
                score_A += 1
            else:
                score_B += 1  #score update
        
        if player_serving == 'A': #Swapping after every match
            player_serving = 'B'
        elif player_serving == 'B':
            player_serving = 'A'
        '''if(score_A>10):
            print("Score A : ",score_A)
            print("Score B : ",score_B)'''
        ret = 'A'
        if(score_B>score_A):
            ret='B'

        if(score_A>500):
            return ret
    return ret

def simulate_matches(pa_values, pb, n):
    winner_serves_wins = []
    alternating_service_wins = []

    for pa in pa_values:
        winner_serves_wins_count = 0
        alternating_service_wins_count = 0
        for _ in range(n):
            winner = winner_serves_match(pa, pb)
            if winner == 'A':
                winner_serves_wins_count += 1

            winner = alternating_service_match(pa, pb)
            if winner == 'A':
                alternating_service_wins_count += 1
        '''if(score_A>20):
            print("Score A : ",score_A)
            print("Score B : ",score_B)'''
        winner_serves_wins.append(winner_serves_wins_count)
        alternating_service_wins.append(alternating_service_wins_count)

    return winner_serves_wins, alternating_service_wins
    
def tennis_match_analysis_with_graph(pa_values, pb, n):
    winner_serves_wins, alternating_service_wins = simulate_matches(pa_values, pb, n)

    plt.plot(pa_values, winner_serves_wins, label="Winner Serves Protocol",marker='o')
    plt.plot(pa_values, alternating_service_wins, label="Alternating Service Protocol",marker='o')
    plt.xticks(pa_values)
    plt.xlabel('Probability of A winning when A is the server (pa)')
    plt.ylabel('Number of Wins for A')
    plt.title('Simulation of Tennis for pb={}'.format(pb))
    plt.legend()
    plt.savefig('o{}.png'.format(pb))
    plt.show()
    
