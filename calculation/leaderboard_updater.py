from script import calculate_match_elos, read_elos
from typing import Dict

def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def read_official_matches(elo_dict: Dict[str,int], matches_txt = "matches.txt", ):
    with open(matches_txt, "r") as file:
        person1 = ""
        person2 = ""
        first = True
        p1_elo_diff_counter = 0
        p2_elo_diff_counter = 0
        for line in file:
            if line == "END":
                print(person1 + ": " + str(p1_elo_diff_counter))
                print(person2 + ": " + str(p2_elo_diff_counter))
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
                    print(old_person1 + ": " + str(p1_elo_diff_counter))
                    print(old_person2 + ": " + str(p2_elo_diff_counter))
                    p1_elo_diff_counter = 0
                    p2_elo_diff_counter = 0


            else:
                p1_diff,p2_diff = calculate_match_elos(person1,person2,int(x[1]),int(x[2]),elo_dict, True)
                p1_elo_diff_counter += p1_diff
                p2_elo_diff_counter += p2_diff





if __name__ == "__main__":
    elo_dict = {}
    read_elos(elo_dict)
    read_official_matches(elo_dict)

    with open("elos.txt", "w") as file:
        for key, value in elo_dict.items():

            file.write(key + "," + str(value) + "\n")