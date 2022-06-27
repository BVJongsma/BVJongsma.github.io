from clue_model import ClueModel

if __name__ == "__main__":
    # Create a Clue model with three players
    model = ClueModel(3, 10, 10)
    # Let the players take turns in a game of Clue
    for i in range(10):
        print(i)
        model.step()