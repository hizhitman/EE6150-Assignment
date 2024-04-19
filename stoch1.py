import matplotlib.pyplot as plt
import numpy as np
from typing import List


def winner_serves_match(pa, pb):
    player_serving = 'A'  # Player A serves first
    score_A = 0
    score_B = 0
    
    while score_A < 5 and score_B < 5:
        if player_serving == 'A':
            if not np.random.choice(2,1,p=[pa,1-pa])[0]: #A wins if this outputs 0
                score_A += 1 #same player repeats
            else:
                score_B += 1 #score update
                player_serving = 'B' #swap for the winner
        else:
            if not np.random.choice(2,1,p=[pb,1-pb])[0]:  #B wins if this outputs 1
                score_A += 1
                player_serving = 'A'  #swap for the winner
            else:
                score_B += 1 #score update #same player repeats
    ret = 'A'
    if(score_B>score_A):
        ret='B'
    return ret


def alternating_service_match(pa, pb):
    score_A = 0
    score_B = 0
    player_serving = 'A'  # Player A serves first
    
    while score_A < 5 and score_B < 5:
        if player_serving == 'A':
            if  not np.random.choice(2,1,p=[pa,1-pa])[0]:
                score_A += 1
            else:
                score_B += 1 #score update
        else:
            if  not np.random.choice(2,1,p=[pb,1-pb])[0]:
                score_A += 1
            else:
                score_B += 1 #score update
        
        if player_serving == 'A':  #swap players
            player_serving = 'B'
        elif player_serving == 'B':
            player_serving = 'A'

    ret = 'A'
    if(score_B>score_A):
        ret='B'
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

        winner_serves_wins.append(winner_serves_wins_count)
        alternating_service_wins.append(alternating_service_wins_count)

    return winner_serves_wins, alternating_service_wins
    
def tennis_match_analysis_with_graph(pa_values: List[float], pb: float, n: int):
    winner_serves_wins, alternating_service_wins = simulate_matches(pa_values, pb, n)

    plt.plot(pa_values, winner_serves_wins, label="Winner Serves Protocol",marker='o')
    plt.plot(pa_values, alternating_service_wins, label="Alternating Service Protocol",marker='o')
    plt.xticks(pa_values)
    plt.xlabel('Probability of A winning when A is the server (pa)')
    plt.ylabel('Number of Wins for A')
    plt.title('Simulation of Tennis for pb={}'.format(pb))
    plt.legend()
    plt.savefig('ig{}.png'.format(pb))
    plt.show()

def dp_simul_winner_serve(pa,pb):
    pw=np.zeros(10);
    pw[0]=pa
    for round in range(1,10):
        pw[round]=pw[round-1]*pa+(1-pw[round-1])*pb  #dp array initialisation

    p9=0
    for i in range(9): #calculating p5, , A loses 4 matches
        p9t=(1-pw[i]) 
        for j in range(i,9):
            if(j!=i):
                p9t1=p9t*(1-pw[j])
                for k in range(j,9):
                    if(k!=i and k!=j):
                        p9t2=p9t1*(1-pw[k])
                        for l in range(k,9):
                            if(l!=i and l!=j and l!=k):
                                p9t3=p9t2*(1-pw[l])
                                for m in range(9):
                                    if(m!=i and m!=j and m!=k  and m!=l):
                                        p9t3*=pw[m]
                                p9+=p9t3

    for i in range(9):#calculating p6, A loses 3 matches
        p9t=(1-pw[i])
        for j in range(i,9):
            if(j!=i):
                p9t1=p9t*(1-pw[j])
                for k in range(j,9):
                    if(k!=i and k!=j):
                        p9t2=p9t1*(1-pw[k])
                        for l in range(9):
                            if(l!=i and l!=j and l!=k):
                                p9t2*=(pw[l])
                        p9+=p9t2

    for i in range(9): #calculating p7, A loses 2 matches
        p9t=(1-pw[i])
        for j in range(i,9):
            if(j!=i):
                p9t1=p9t*(1-pw[j])
                for k in range(9):
                    if(k!=i and k!=j):
                        p9t1*=(pw[k])
                p9+=p9t1

    for i in range(9): #calculating p8, A loses only 1 match
        p9t=(1-pw[i])
        for j in range(9):
            if(j!=i):
                p9t*=(pw[j])
        p9+=p9t

    p9t=1   #calculating p9, A wins all 9 matches
    for i in range(9):
        p9t*=(pw[i])
    p9+=p9t

#Care has been taken to ensure there are no overlaps between the 5 probabilities calculated
    p_final = (p9)
    # print(p_final)
    # print(pw)
    return p_final

def dp_simul_alternate_serve(pa,pb):
    pw=np.zeros(10);
    for round in range(0,10):
        if(round%2):
            pw[round]=pb
        else:
            pw[round]=pa

    

    p9=0
    for i in range(9):
        p9t=(1-pw[i])
        for j in range(i,9):
            if(j!=i):
                p9t1=p9t*(1-pw[j])
                for k in range(j,9):
                    if(k!=i and k!=j):
                        p9t2=p9t1*(1-pw[k])
                        for l in range(k,9):
                            if(l!=i and l!=j and l!=k):
                                p9t3=p9t2*(1-pw[l])
                                for m in range(9):
                                    if(m!=i and m!=j and m!=k  and m!=l):
                                        p9t3*=pw[m]
                                p9+=p9t3

    for i in range(9):
        p9t=(1-pw[i])
        for j in range(i,9):
            if(j!=i):
                p9t1=p9t*(1-pw[j])
                for k in range(j,9):
                    if(k!=i and k!=j):
                        p9t2=p9t1*(1-pw[k])
                        for l in range(9):
                            if(l!=i and l!=j and l!=k):
                                p9t2*=(pw[l])
                        p9+=p9t2

    for i in range(9):
        p9t=(1-pw[i])
        for j in range(i,9):
            if(j!=i):
                p9t1=p9t*(1-pw[j])
                for k in range(9):
                    if(k!=i and k!=j):
                        p9t1*=(pw[k])
                p9+=p9t1

    for i in range(9):
        p9t=(1-pw[i])
        for j in range(9):
            if(j!=i):
                p9t*=(pw[j])
        p9+=p9t

    p9t=1
    for i in range(9):
        p9t*=(pw[i])
    p9+=p9t


    p_final = (p9)
    # print(p_final)
    # print(pw)
    return p_final

def final_dp(pa_values,pb,n):
    winner_serves_wins,alternating_service_wins=[],[]
    for pa in pa_values:
        winner_serves_wins.append(dp_simul_winner_serve(pa,pb)*n)
        alternating_service_wins.append(dp_simul_alternate_serve(pa,pb)*n)
        
    plt.plot(pa_values, winner_serves_wins, label="Winner Serves Protocol",marker='o')
    plt.plot(pa_values, alternating_service_wins, label="Alternating Service Protocol",marker='o')
    plt.xticks(pa_values)
    plt.xlabel('Probability of A winning when A is the server (pa)')
    plt.ylabel('Number of Wins for A')
    plt.title('Analytical solution for pb={}'.format(pb))
    plt.legend()
    plt.savefig('imag{}.png'.format(pb))
    plt.show()
        
                
    
