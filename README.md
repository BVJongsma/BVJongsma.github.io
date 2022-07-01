# Implementation
### The different strategies
Agents can ask other agents about what cards they have. What kind of questions they ask, is according to which strategy they follow.
The different strategies are as following:
* RANDOM: The agent asks for a random weapon and random suspect card.
* NOT_OWN: The agent asks for two cards that they themselves don't own.
* ONE_OWN:  The agent asks for one card that they have themselves, and one card that they don't own themselves.
* UNKNOWN: The agent asks for two cards that they don't know to who they belong.
* ONE_UNKNOWN: The agent asks about one card that they know where it is, and one card that they don't know where it is.
* REASONING: The agent asks about one card that they know about and isn't of the next agent, and one card that might be of the next
            agent or in the envelope (or if there are none such cards: that might be of the next agent)
### Running the implementation
Our code was tested with `python3.9` on Ubuntu and Windows.
Various python packages where used that can be obtained via pip. For the exact programs, see [the requirements file](requirements.txt).

The code builds on [mlsolver](https://github.com/erohkohl/mlsolver) which is included in the repository.

Running the implementation goes as follows:

1. Please make sure all required packages are installed.
2. The `Implementation/src/main.py` program can be run, either from the command line or by using bash.
    It does not require additional input, but a few global boolean values can be set in the main.py.
   * SHORT_RUN (default: True): Play one game. The interface is then only shown for this game.
    * DIFFERENT_STRATEGIES: Run all combinations of strategies against each other. Agent 1 has one strategy, agent 2 and 3 both have another stategy.
    * STRAT_VS_RANDOM: Agent 1 has a different strategy every time, while both Agent 2 and Agent 3 have the 'RANDOM' strategy.
    * ENTER (default: False): If this is set to True, you need to continually press enter before the next turn is taken.
    * NUM_WEAPONS (default: 4). This is the total amount of weapon cards, and can be set to either 4 or 7.
    * NUM_SUSPECTS (default: 4). This is the total amount of suspect cards, and can be set to either 4 or 7.

    Please note that setting either NUM_WEAPONS or NUM_SUSPECTS significantly slows down the model,
especially the interface. While it does work, we don't recommend setting NUM_WEAPONS or NUM_SUSPECTS to 7 in
   combination with SHORT_RUN = True.

# Program and File Structure
## Implementation
### Results
This contains some text files where the results from our experiments are ran.
### src
This contains all the necessary files to run the implementation.
## docs
All files related to the creation of the website are contained here.
### figures
All figures related to the website are contained in this folder.
