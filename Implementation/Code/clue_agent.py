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
        # TODO remove relations based on agent's cards

    # Set the agent that is next in turn and that a suggestion is made to
    def initialise_next_agent(self):
        next_agent_id = self.unique_id + 1
        if (next_agent_id > self.model.get_num_agents()):
            next_agent_id = 1
        self.next_agent = self.model.get_agent_from_id(next_agent_id)

    # Get the current agent's ID
    def get_unique_id(self):
        return self.unique_id

    # Get a response of the current agent based on the suggestion that is made
    # TODO Current implementation: show any of the suggested cards at random
    def get_response(self, suggestion):
        possible_response_cards = list(set(self.agent_cards).intersection(suggestion))
        if (len(possible_response_cards) < 1):
            response_card = None
        else:
            response_card = random.choice(possible_response_cards)
        return response_card

    # Take a turn
    # TODO what does an agent do during a step
    def step(self):
        print("This is agent " + str(self.unique_id) + ".")
        print("With cards " + str(self.agent_cards) + ".")
        # Let the current agent make a suggestion
        # TODO Current implementation: pick suggestion at random
        suggestion = [self.cards.get_random_weapon()] + [self.cards.get_random_suspect()]
        print("They suggest " + str(suggestion) + ".")
        print("The agent they suggest to is agent " + str(self.next_agent.get_unique_id()) + ".")
        # Get a response from the next agent with whether or not they have any of the cards
        response = self.next_agent.get_response(suggestion)
        print("Their response is " + str(self.next_agent.get_response(suggestion)) + ".")
        # Update the knowledge of the agents based on the suggestion and response
        self.update_knowledge(suggestion, response)
        # Check if there is a winner
        self.model.check_end_state()

    # Update the knowledge of all agents via a public or private announcement
    # TODO move to clue_model?
    def update_knowledge(self, suggestion, response):
        if response is None: # Next agent does not have any of the cards
            # Publicly announce that next agent does not have any
            self.model.publicly_announce(self.next_agent, suggestion, False)
        else: # Next agent does have one of the cards
            # Publicly announce that next agent does have one
            self.model.publicly_announce(self.next_agent, suggestion, True)
            # Privately announce the card of next agent to this self agent
