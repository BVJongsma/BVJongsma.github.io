import mesa
from mesa import space
from mesa import time

from Implementation.src.clue_agent import ClueAgent
from Implementation.src.envelope_agent import EnvelopeAgent
from Implementation.src.cards import Cards
from Implementation.src.mlsolver.model import Clue
from Implementation.src.mlsolver.formula import Atom, And, Not, Or, Box, Box_a, Box_star

class ClueModel(mesa.Model):
    """A model with some number of agents."""

    # TODO do we want width and height, currently not used.
    def __init__(self, N, width, height):
        self.num_agents = N
        self.cards = Cards(self.num_agents)
        self.grid = mesa.space.MultiGrid(width, height, True)
        # The agents activate one at a time, in the order they were added.
        self.schedule = mesa.time.BaseScheduler(self)
        self.running = True
        self.envelope = self.initialise_envelope()
        self.agents = self.initialise_agents()
        self.kripke_model = Clue(self.cards, self.num_agents, self)

        # For each agent, determine the next agent in turn, which is also the agent they suggest to
        for agent in self.agents:
            agent.initialise_next_agent()
            # agent.update_kripke_initial_cards()


        # TODO: way to collect data, and easily print things. This is from introduction to MESA example.
        # self.datacollector = mesa.datacollection.DataCollector(
        #     model_reporters={"Gini": compute_gini}, agent_reporters={"Wealth": "wealth"}
        # )

    # Initialise the case file envelope
    def initialise_envelope(self):
        # Get the envelope's cards, which consist of a weapon card and a suspect card
        envelope_cards = [self.cards.get_envelope_weapon()]
        envelope_cards.append(self.cards.get_envelope_suspect())
        # Sort the cards alphabetically
        envelope_cards = sorted(envelope_cards, key = str.lower)
        return EnvelopeAgent(0, envelope_cards, self)

    # Initialise the players (agents)
    def initialise_agents(self):
        agents = []
        for i in range(self.num_agents):
            # Get the agent's cards
            agent_cards = self.cards.get_agent_cards()
            if i == 0:
                a = ClueAgent(i+1, self.cards, agent_cards, "UNKNOWN", self)
            else:
                a = ClueAgent(i+1, self.cards, agent_cards, "RANDOM", self)
            # Add the agent to the MESA schedule, so it can take a turn
            self.schedule.add(a)
            agents.append(a)
            # TODO do we want to add the agents to a grid?
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
        return agents

    # Get the number of players (agents) in the game
    def get_num_agents(self):
        return self.num_agents

    def get_cards(self):
        return self.cards

    # Get an agent's ID
    def get_agent_from_id(self, agent_id):
        return self.agents[agent_id - 1]

    # Get the Kripke Model that contains the knowledge present in the model
    def get_kripke_model(self):
        return self.kripke_model
    #
    # # Make a public announcement
    # # type Agent: 'Implementation.src.clue_agent.ClueAgent'
    # # type suggestion"list of strings
    # def publicly_announce(self, agent, suggestion, affirmed):
    #     if affirmed: # agent did have one or more of the suggested cards
    #         # Go through all card possibilities
    #         # Delete the possibilities where neither of the suggested cards are present
    #         for card_1 in self.cards.get_all_cards():
    #             for card_2 in self.cards.get_all_cards():
    #                 if card_1 not in suggestion and card_2 not in suggestion:
    #                     for a in self.agents:
    #                         announcement = Not(Atom(str(agent.get_unique_id()) + ":" + str(sorted([card_1, card_2],
    #                                                                                               key = str.lower))))
    #                         self.kripke_model.get_kripke_structure().relation_solve(a, announcement)
    #
    #     else: # agent has none of the suggested cards (affirmed = False)
    #         # Go through the two suggested cards (agent has neither of these)
    #         for suggested_card in suggestion:
    #             # Make pairs with this suggested card and any other card
    #             for other_card in self.cards.get_all_cards():
    #                 # For each agent, make + solve announcement
    #                 for a in self.agents:
    #                     announcement = Not(Atom(str(agent.get_unique_id()) + ":" + str(sorted([suggested_card, other_card], key = str.lower))))
    #                     self.kripke_model.get_kripke_structure().relation_solve(a, announcement)

    # Make a public announcement
    # type Agent: 'Implementation.src.clue_agent.ClueAgent'
    # type suggestion"list of strings
    # New implementation
    def publicly_announce(self, asking_agent, agent, suggestion, affirmed):
        if affirmed:  # agent did have one or more of the suggested cards
            # TODO implementation for suggesting 3 cards instead of 2
            announcement = Or(Atom(suggestion[0]), Atom(suggestion[1]))
            print("announcement", announcement)
            updating_agent = agent.next_agent
            asked_agent_id = agent.get_unique_id()
            self.kripke_model.get_kripke_structure().relation_solve(updating_agent, announcement, asked_agent_id)

        else:  # agent has none of the suggested cards (affirmed = False)
            announcement = And(Not(Atom(suggestion[0])), Not(Atom(suggestion[1])))
            print("announcement", announcement)
            updating_agent = agent.next_agent
            asked_agent_id = agent.get_unique_id()
            # Update the relations for the agent that asked for the cards.
            self.kripke_model.get_kripke_structure().relation_solve(asking_agent, announcement, asked_agent_id)
            # Update the relations for the agent that did not ask for the cards.
            self.kripke_model.get_kripke_structure().relation_solve(updating_agent, announcement, asked_agent_id)

    # Check if there is a winner of the game
    # TODO what if there are multiple agents that win at the same time?
    def check_end_state(self):
        winner, guess = self.kripke_model.find_winner()
        if winner == []:
            return
        else:
            print("GAME FINISHED")
            print("Winner is player " + str(winner))
            print("According to this player, the envelope consists of: " + str(guess))
            print("The envelope consists of: " + str(self.envelope.get_envelope_cards()))
            exit()

    # Let the agents take turns
    def step(self):
        # self.datacollector.collect(self)
        self.schedule.step()
