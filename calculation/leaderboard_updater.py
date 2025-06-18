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
        for line in file:
            x = line.split(",")
            if is_integer(x[0]):
                person1 = x[1].strip()
                person2 = x[2].strip()

            else:
                calculate_match_elos(person1,person2,int(x[1]),int(x[2]),elo_dict)




if __name__ == "__main__":
    elo_dict = {}
    read_elos(elo_dict)
    read_official_matches(elo_dict)

    with open("elos.txt", "w") as file:
        for key, value in elo_dict.items():
            file.write(key + "," + str(value) + "\n")