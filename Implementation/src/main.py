from clue_model import ClueModel
import interface.interface as inf

SHORT_RUN = False
DIFFERENT_STRATEGIES = True
NUM_WEAPONS = 7
NUM_SUSPECTS = 4

if __name__ == "__main__":
    if SHORT_RUN:
        strat_agent1 = "RANDOM"
        strat_other_agents = "RANDOM"
        clue_model = ClueModel(3, NUM_WEAPONS, NUM_SUSPECTS, strat_agent1, strat_other_agents)
        # interface = inf.GameInterface(clue_model)
        # Create a Clue model with three players
        # Let the players take turns in a game of Clue
        turn = 0
        while not clue_model.check_end_state():
            print(turn)
            # input("press enter to continue")
            clue_model.step()
            turn += 1

        # TODO only ends if interface is turned off.
    if DIFFERENT_STRATEGIES:
        strats = ["RANDOM", "NOT_OWN", "ONE_OWN", "UNKNOWN", "ONE_UNKNOWN", "REASONING"]
        for strat_agent1 in strats:
            for strat_other_agents in strats:
                print("Agent 1: " + strat_agent1 + " ,other agents: " + strat_other_agents)
                clue_model = ClueModel(3, NUM_WEAPONS, NUM_SUSPECTS, strat_agent1, strat_other_agents)
                # interface = inf.GameInterface(clue_model)
                # Create a Clue model with three players
                # Let the players take turns in a game of Clue
                turn = 0
                while not clue_model.check_end_state():
                    print(turn)
                    # input("press enter to continue")
                    clue_model.step()
                    turn += 1
