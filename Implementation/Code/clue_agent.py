import random

import mesa


class ClueAgent(mesa.Agent):
    """An agent who plays the game of Clue."""

    def __init__(self, unique_id, cards, agent_cards, model):
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.cards = cards
        self.agent_cards = agent_cards
        self.model = model
        self.next_agent = None

    def initialise_next_agent(self):
        next_agent_id = self.unique_id + 1
        if (next_agent_id > self.model.get_num_agents()):
            next_agent_id = 1
        self.next_agent = self.model.get_agent_from_id(next_agent_id)

    def get_unique_id(self):
        return self.unique_id

    # Current implementation: show any of the suggested cards at random
    def get_response(self, suggestion):
        possible_response_cards = list(set(self.agent_cards).intersection(suggestion))
        if (len(possible_response_cards) < 1):
            response_card = None
        else:
            response_card = random.choice(possible_response_cards)
        return response_card

    # During a step, the agent will ask another agent if they have a card.
    # TODO what does an agent do during a step
    def step(self):
        print("This is agent " + str(self.unique_id) + ".")
        print("With cards " + str(self.agent_cards) + ".")
        # Current implementation: pick suggestion at random
        suggestion = [self.cards.get_random_weapon()] + [self.cards.get_random_suspect()]
        print("They suggest " + str(suggestion) + ".")
        # TODO ask other agent
        print("The agent they suggest to is agent " + str(self.next_agent.get_unique_id()) + ".")
        print("Their response is " + str(self.next_agent.get_response(suggestion)) + ".")

        # TODO update knowledge for all