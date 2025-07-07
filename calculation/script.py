
import math
from typing import Dict



def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

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

def calculate_match_elos(person1: str, person2: str, p1score: int, p2score: int, elo_dict: Dict[str, int], difference: bool):

    #-----------CONFIG-------------------#
    overall_multiplier = 40
    score_significance_multiplier= -3.4
    elo_significance_modifier = 400
    #------------------------------------#

    p1_elo = elo_dict[person1]
    p2_elo = elo_dict[person2]

    old_p1_elo = p1_elo
    old_p2_elo = p2_elo

    q1 = math.pow(10, (p1_elo/elo_significance_modifier)) #elo significance modifier
    q2 = math.pow(10, (p2_elo/elo_significance_modifier))

    expected_value1 = q1/(q1+q2)

    actual_value1 = 1/(1+math.pow(math.e, score_significance_multiplier * ((p1score-p2score) / p2score))) #score significance modifier

    expected_value2 = 1 - expected_value1
    actual_value2 = 1 - actual_value1



    if (actual_value1 - expected_value1) <= 0: #if player 1 did worse than expected
        if actual_value1 >= 0.5: #if player 1 won the game
            pass
        else: # if player 1 lost the game
            p1_elo = p1_elo + overall_multiplier * (actual_value1 - expected_value1) #overall modifier
    else: #if player 1 did better than expected
        if actual_value1 > 0.5: #if player 1 won the game
            p1_elo = p1_elo + overall_multiplier * (actual_value1 - expected_value1)
        else: #if player 1 lost the game
            pass


    if (actual_value2 - expected_value2) <= 0: #if player 2 did worse than expected
        if actual_value2 >= 0.5: #if player 2 won or tied the game
            pass
        else: # if player 2 lost the game
            p2_elo = p2_elo + overall_multiplier * (actual_value2 - expected_value2)
    else: #if player 2 did better than expected
        if actual_value2 > 0.5: #if player 2 won or tied the game
            p2_elo = p2_elo + overall_multiplier * (actual_value2 - expected_value2)
        else: #if player 2 lost the game
            pass


    elo_dict[person1] = round(p1_elo)
    elo_dict[person2] = round(p2_elo)

    if difference:
        p1_diff = round(p1_elo - old_p1_elo)
        p2_diff = round(p2_elo - old_p2_elo)

        return p1_diff,p2_diff
    return None

def calculate_wins(matches_txt: str) -> Dict[str, int]:
    with open(matches_txt, "r") as file:
        person1 = ""
        person2 = ""
        first = True
        match_differential = 0
        wl_dict = {}
        for line in file:
            if line == "END":
                wl_dict[person1] = match_differential
                wl_dict[person2] = -1 * match_differential
                continue
            x = line.split(",")
            if is_integer(x[0]):
                old_person1 = person1
                old_person2 = person2
                person1 = x[1].strip()
                person2 = x[2].strip()
                if first:
                    first = False
                    continue
                else:
                    wl_dict[old_person1] = match_differential
                    wl_dict[old_person2] = -1 * match_differential
                    match_differential = 0

            else:
                if int(x[1]) > int(x[2]):  # person 1 won

                    match_differential += 1
                if int(x[1]) < int(x[2]):  # person 2 won

                    match_differential -= 1
    return wl_dict

if __name__ == '__main__':
    elo_dict = {}
    matches = []
    read_elos(elo_dict)
    read_matches()

    print("Before: " + str(elo_dict))
    i = 1
    for match in matches:
        calculate_match_elos(match[0],match[1],int(match[2]),int(match[3]), elo_dict, True)

        print("After match " + str(i) + ": " + str(elo_dict)) #for individual elo changes
        i += 1

    with open("elos.txt","w") as file:
        for key, value in elo_dict.items():
            file.write(key + "," + str(value) + "\n")




