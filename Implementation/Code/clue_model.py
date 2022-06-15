import mesa
from mesa import space
from mesa import time


class EnvelopeAgent(mesa.Agent):
    """The envelope containing the murder weapon and killer cards."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


class ClueAgent(mesa.Agent):
    """An agent who plays the game of Clue."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    # During a step, the agent will ask another agent if they have a card.
    # TODO what does an agent do during a step
    def step(self):
        print("This is agent " + str(self.unique_id) + ".")


class ClueModel(mesa.Model):
    """A model with some number of agents."""

    # TODO do we want width and height, currently not used.
    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, True)
        # The agents activate one at a time, in the order they were added.
        self.schedule = mesa.time.BaseScheduler(self)
        self.running = True

        # Create the envelope. This agent is not added to the schedule.
        # TODO we do not want this agent to have a step, but how do we actually use it. Is it possible to not have this
        #  agent or initialise it in some other way?
        a = EnvelopeAgent(0, self)

        # Create playing agents.
        for i in range(self.num_agents):
            a = ClueAgent(i+1, self)
            self.schedule.add(a)
            # TODO do we want to add the agents to a grid?
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        # TODO: way to collect data, and easily print things. This is from introduction to MESA example.
        # self.datacollector = mesa.datacollection.DataCollector(
        #     model_reporters={"Gini": compute_gini}, agent_reporters={"Wealth": "wealth"}
        # )

    def step(self):
        # self.datacollector.collect(self)
        self.schedule.step()
