import mesa


class ClueAgent(mesa.Agent):
    """An agent who plays the game of Clue."""

    def __init__(self, unique_id, cards, agent_cards, model):
        super().__init__(unique_id, model)
        self.cards = cards
        self.agent_cards = agent_cards

    # During a step, the agent will ask another agent if they have a card.
    # TODO what does an agent do during a step
    def step(self):
        print("This is agent " + str(self.unique_id) + ".")
        print("With cards " + str(self.agent_cards) + ".")
        # TODO pick suggestion
        # TOOO ask other agent
        # TODO update knowledge for all