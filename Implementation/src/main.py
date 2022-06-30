from clue_model import ClueModel
import interface.interface as inf

# Set variables to True or False for different player strategies/ gathering data.
SHORT_RUN = False
DIFFERENT_STRATEGIES = False
STRAT_VS_RANDOM = True
# Select the number of weapons and suspects (set to 4 or 7)
NUM_WEAPONS = 7
NUM_SUSPECTS = 4


# One run with some selected strategies.
def run(strategy_agent1, strategy_other_agents):
    # Create a Clue model with three players
    clue_model = ClueModel(3, NUM_WEAPONS, NUM_SUSPECTS, strategy_agent1, strategy_other_agents)
    # Uncomment to show the interface.
    # interface = inf.GameInterface(clue_model)
    # Let the players take turns in a game of Clue
    turn = 0
    while not clue_model.check_end_state():
        print(turn)
        # Uncomment if you want to press enter before continuing with the next step.
        # input("press enter to continue")
        clue_model.step()
        turn += 1


# Function for running code next to interface for some other part.
def next_to_interface():
    # Loop over different strategies and run for all combinations.
    if DIFFERENT_STRATEGIES:
        strats = ["RANDOM", "NOT_OWN", "ONE_OWN", "UNKNOWN", "ONE_UNKNOWN", "REASONING"]
        for strategy_agent1 in strats:
            for strategy_other_agents in strats:
                print("------------------------------------------------------------------------")
                print("Agent 1: " + strategy_agent1 + ", other agents: " + strategy_other_agents)
                run(strategy_agent1, strategy_other_agents)

    # Loop over different strategies and run a strategy versus random.
    if STRAT_VS_RANDOM:
        strats = ["NOT_OWN", "ONE_OWN", "UNKNOWN", "ONE_UNKNOWN", "REASONING"]
        strategy_other_agents = "RANDOM"
        for strategy_agent1 in strats:
            print("------------------------------------------------------------------------")
            print("Agent 1: " + strategy_agent1 + ", other agents: " + strategy_other_agents)
            run(strategy_agent1, strategy_other_agents)


if __name__ == "__main__":
    # One short run where all agents use a random approach.
    if SHORT_RUN:
        strat_agent1 = "RANDOM"
        strat_other_agents = "RANDOM"
        run(strat_agent1, strat_other_agents)

        next_to_interface()
    next_to_interface()

