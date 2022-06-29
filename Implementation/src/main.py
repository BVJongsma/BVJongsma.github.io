from clue_model import ClueModel
import interface.interface as inf

if __name__ == "__main__":
    interface = inf.GameInterface(3)
    # Create a Clue model with three players
    num_weapons = 4  # Can also be 7
    num_suspects = 4
    model = ClueModel(3, 10, 10) # num_weapons, num_suspects)
    # Let the players take turns in a game of Clue
    # TODO use end game function instead of range(10)
    for i in range(10):
        print(i)
        model.step()
