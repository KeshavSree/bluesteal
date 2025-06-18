
import math
from typing import Dict





def read_elos(elo_dict: Dict[str, int]):
    with open("elos.txt", "r") as file:
        for line in file:
            x = line.split(",")
            elo_dict[x[0]] = int(x[1])

def read_matches():
    with open("matches.txt", "r") as file:
        for line in file:
            x = line.split(",")
            match = (x[0],x[1],x[2],x[3])
            matches.append(match)

def calculate_match_elos(person1: str, person2: str, p1score: int, p2score: int, elo_dict: Dict[str, int]):
    p1_elo = elo_dict[person1]
    p2_elo = elo_dict[person2]

    q1 = math.pow(10, (p1_elo/400)) #elo significance modifier
    q2 = math.pow(10, (p2_elo/400))

    expected_value1 = q1/(q1+q2)

    actual_value1 = 1/(1+math.pow(math.e, -4.4 * ((p1score-p2score) / p2score))) #score significance modifier

    expected_value2 = 1 - expected_value1
    actual_value2 = 1 - actual_value1


    if (actual_value1 - expected_value1) <= 0: #if player 1 did worse than expected
        if actual_value1 >= 0.5: #if player 1 won the game
            pass
        else: # if player 1 lost the game
            p1_elo = p1_elo + 100 * (actual_value1 - expected_value1) #overall modifier
    else: #if player 1 did better than expected
        if actual_value1 > 0.5: #if player 1 won the game
            p1_elo = p1_elo + 100 * (actual_value1 - expected_value1)
        else: #if player 1 lost the game
            pass


    if (actual_value2 - expected_value2) <= 0: #if player 2 did worse than expected
        if actual_value2 >= 0.5: #if player 2 won or tied the game
            pass
        else: # if player 2 lost the game
            p2_elo = p2_elo + 100 * (actual_value2 - expected_value2)
    else: #if player 2 did better than expected
        if actual_value2 > 0.5: #if player 2 won or tied the game
            p2_elo = p2_elo + 100 * (actual_value2 - expected_value2)
        else: #if player 2 lost the game
            pass


    elo_dict[person1] = round(p1_elo)
    elo_dict[person2] = round(p2_elo)


if __name__ == '__main__':
    elo_dict = {}
    matches = []
    read_elos(elo_dict)
    read_matches()

    print("Before: " + str(elo_dict))
    i = 1
    for match in matches:
        calculate_match_elos(match[0],match[1],int(match[2]),int(match[3]), elo_dict)

        print("After match " + str(i) + ": " + str(elo_dict)) #for individual elo changes
        i += 1

    with open("elos.txt","w") as file:
        for key, value in elo_dict.items():
            file.write(key + "," + str(value) + "\n")




