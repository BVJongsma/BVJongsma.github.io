from clue_model import ClueModel
import interface.interface as inf

if __name__ == "__main__":
    model = ClueModel(3, 10, 10)
    interface = inf.GameInterface(model)
    # Create a Clue model with three players
    # Let the players take turns in a game of Clue
    for i in range(10):
        print(i)
        input("press enter to continue")
        model.step()