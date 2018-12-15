from levenshtein import distance
from speech import listen_to_input


def act_on_input(input_str):
    input_list = input_str.split()
    cmd = input_list[0]
    if distance(cmd, "appel") <= 2:
        print("Bien reçu, j'appelle ".format("".join(input_list[1:])))
    elif distance(cmd, "alert") <= 2:
        print("Bien reçu, je mets une alerte ici sur ".format("".join(input_list[1:])))
    elif distance(cmd, "info") <= 2:
        print("Bien reçu, voilà les infos sur ".format("".join(input_list[1:])))


if __name__ == "__main__":
    listen_to_input(act_on_input)
