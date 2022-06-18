import mesa
from mesa import space
from mesa import time

from Implementation.Code.clue_agent import ClueAgent
from Implementation.Code.envelope_agent import EnvelopeAgent
from Implementation.Code.cards import Cards
from Implementation.Code.mlsolver.model import Clue


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
        for agent in self.agents:
            agent.initialise_next_agent()

        # TODO: way to collect data, and easily print things. This is from introduction to MESA example.
        # self.datacollector = mesa.datacollection.DataCollector(
        #     model_reporters={"Gini": compute_gini}, agent_reporters={"Wealth": "wealth"}
        # )

    def initialise_envelope(self):
        # Create the envelope. This agent is not added to the schedule.
        # TODO we do not want this agent to have a step, but how do we actually use it. Is it possible to not have this
        #  agent or initialise it in some other way?
        envelope_cards = [self.cards.get_envelope_weapon()]
        envelope_cards = envelope_cards.append(self.cards.get_envelope_suspect())

        return EnvelopeAgent(0, envelope_cards, self)

    def initialise_agents(self):
        agents = []
        # Create playing agents.
        for i in range(self.num_agents):
            agent_cards = self.cards.get_agent_cards()
            a = ClueAgent(i+1, self.cards, agent_cards, self)
            self.schedule.add(a)
            agents.append(a)
            # TODO do we want to add the agents to a grid?
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
        return agents

    def get_num_agents(self):
        return self.num_agents

    def get_agent_from_id(self, agent_id):
        return self.agents[agent_id - 1]

    def step(self):
        # self.datacollector.collect(self)
        self.schedule.step()
