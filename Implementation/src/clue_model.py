import mesa
from mesa import time

from Implementation.src.clue_agent import ClueAgent
from Implementation.src.envelope_agent import EnvelopeAgent
from Implementation.src.cards import Cards
from Implementation.src.mlsolver.model import Clue
from Implementation.src.mlsolver.formula import Atom, And, Not, Or

PRINT = True

class ClueModel(mesa.Model):
    """A model with some number of agents."""

    # Initialise the model.
    def __init__(self, N, num_weapons, num_suspects, strat_agent1, strat_other_agents):
        self.num_agents = N
        self.num_weapons = num_weapons
        self.num_suspects = num_suspects
        self.cards = Cards(self.num_agents, num_weapons, num_suspects)
        # The agents activate one at a time, in the order they were added.
        self.schedule = mesa.time.BaseScheduler(self)
        self.running = True
        self.envelope = self.initialise_envelope()
        self.agents = self.initialise_agents(strat_agent1, strat_other_agents)
        self.kripke_model = Clue(self.cards, self.num_agents, self)

        # For each agent, determine the next agent in turn, which is also the agent they suggest to
        for agent in self.agents:
            agent.initialise_next_agent()

        # Initialise the dictionary using the cards each player has.
        self.knowledge_dict, self.unknown_cards = self.kripke_model.initialise_known_dictionary(self.agents)
        if PRINT:
            print(self.unknown_cards)
            print(self.knowledge_dict)

    # Initialise the case file envelope
    def initialise_envelope(self):
        # Get the envelope's cards, which consist of a weapon card and a suspect card
        envelope_cards = [self.cards.get_envelope_weapon(), self.cards.get_envelope_suspect()]
        # Sort the cards alphabetically
        envelope_cards = sorted(envelope_cards, key=str.lower)
        return EnvelopeAgent(0, envelope_cards, self)

    # Initialise the players (agents)
    def initialise_agents(self, strat_agent1, strat_other_agents):
        agents = []
        for i in range(self.num_agents):
            # Get the agent's cards
            agent_cards = self.cards.get_agent_cards()
            if i == 0:
                a = ClueAgent(i + 1, self.cards, agent_cards, strat_agent1, self, "SHOWN")
            else:
                a = ClueAgent(i + 1, self.cards, agent_cards, strat_other_agents, self, "SHOWN")
            # Add the agent to the MESA schedule, so it can take a turn
            self.schedule.add(a)
            agents.append(a)
        return agents

    # Get the number of players (agents) in the game
    def get_num_agents(self):
        return self.num_agents

    # Get the cards that are in the game.
    def get_cards(self):
        return self.cards

    # Get an agent's ID
    def get_agent_from_id(self, agent_id):
        return self.agents[agent_id - 1]

    # Get the Kripke Model that contains the knowledge present in the model
    def get_kripke_model(self):
        return self.kripke_model

    # Get the knowledge dictionary.
    def get_knowledge_dict(self):
        return self.knowledge_dict

    # Get the unknown cards for an agent.
    def get_unknown_cards(self, agent_id):
        return self.unknown_cards[agent_id]

    # Make a public announcement
    def publicly_announce(self, asking_agent, agent, suggestion, affirmed):
        if affirmed:  # agent did have one or more of the suggested cards
            announcement = Or(Atom(suggestion[0]), Atom(suggestion[1]))  # A \lor B
            if PRINT:
                print("public announcement", announcement)
            updating_agent = agent.next_agent
            asked_agent_id = agent.get_unique_id()
            self.kripke_model.get_kripke_structure().relation_solve(updating_agent, announcement, asked_agent_id)

        else:  # agent has none of the suggested cards (affirmed = False)
            announcement = And(Not(Atom(suggestion[0])), Not(Atom(suggestion[1])))  # \neg A \land \neg B
            if PRINT:
                print("public announcement", announcement)
            updating_agent = agent.next_agent
            asked_agent_id = agent.get_unique_id()
            # Update the relations for the agent that asked for the cards.
            self.kripke_model.get_kripke_structure().relation_solve(asking_agent, announcement, asked_agent_id)
            # Update the relations for the agent that did not ask for the cards.
            self.kripke_model.get_kripke_structure().relation_solve(updating_agent, announcement, asked_agent_id)

    # Update the knowledge dictionary.
    def update_knowledge_dict(self):
        self.knowledge_dict, self.unknown_cards = self.kripke_model.update_knowledge_dictionary(self.knowledge_dict,
                                                                                                self.unknown_cards)

    # Check if there is a winner of the game.
    def check_end_state(self):
        winner, guess = self.kripke_model.find_winner()
        if not winner:
            return False
        else:
            if PRINT:
                print("GAME FINISHED")
                print("Winner is player " + str(winner))
                print("According to this player, the envelope consists of: " + str(guess))
                print("The envelope consists of: " + str(self.envelope.get_envelope_cards()))
            return True

    # Get the agents in the game.
    def get_agents(self):
        return self.agents

    # Let the agents take turns
    def step(self):
        if not self.check_end_state():
            self.schedule.step()
