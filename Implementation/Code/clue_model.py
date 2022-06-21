import mesa
from mesa import space
from mesa import time

from Implementation.Code.clue_agent import ClueAgent
from Implementation.Code.envelope_agent import EnvelopeAgent
from Implementation.Code.cards import Cards
from Implementation.Code.mlsolver.model import Clue
from Implementation.Code.mlsolver.formula import Atom, And, Not, Or, Box_a, Box_star


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
        self.kripke_model = Clue(self.cards, self.num_agents)

        # TODO Does this go here?
        # For each agent, determine the next agent in turn, which is also the agent they suggest to
        for agent in self.agents:
            agent.initialise_next_agent()

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
            a = ClueAgent(i+1, self.cards, agent_cards, self)
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

    # Get an agent's ID
    def get_agent_from_id(self, agent_id):
        return self.agents[agent_id - 1]

    # Get the Kripke Model that contains the knowledge present in the model
    def get_kripke_model(self):
        return self.kripke_model

    # Make a public announcement
    def publicly_announce(self, agent, suggestion, affirmed):
        if affirmed: # agent did have one of the suggested cards
            announcement = Box_a('3', Atom('3:'))
        else: # agent has none of the suggested cards
            announcement = Box_a('3', Atom('3:'))

        self.kripke_model.get_kripke_structure().relation_solve(agent, announcement)

    # Check if there is a winner of the game
    def check_end_state(self):
        return

    # Let the agents take turns
    def step(self):
        # self.datacollector.collect(self)
        self.schedule.step()
