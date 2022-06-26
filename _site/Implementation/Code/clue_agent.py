import random
import mesa
from Implementation.Code.mlsolver.formula import Atom, And, Not, Or, Box_a, Box_star

# Strategy
# Suggest randomly
RANDOM = False
# Use neither of your own cards in suggestion
NOT_OWN = False
# Use one of your own cards in suggestion
ONE_OWN = True
# TODO
ELIMINATING = False

class ClueAgent(mesa.Agent):
    """An agent who plays the game of Clue."""

    def __init__(self, unique_id, cards, agent_cards, model):
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.cards = cards
        self.agent_cards = agent_cards
        self.model = model
        self.next_agent = None

    def update_kripke_initial_cards(self):
        announcement = Atom(str(self.get_unique_id()) + ":" + str(self.agent_cards))
        self.model.get_kripke_model().get_kripke_structure().relation_solve(self, announcement)

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
    def step(self):
        print("This is agent " + str(self.unique_id) + ".")
        print("With cards " + str(self.agent_cards) + ".")
        # Let the current agent make a suggestion
        # TODO Current implementation: pick suggestion at random
        suggestion = self.pick_suggestion()
        print("They suggest " + str(suggestion) + ".")
        print("The agent they suggest to is agent " + str(self.next_agent.get_unique_id()) + ".")
        # Get a response from the next agent with whether or not they have any of the cards
        response = self.next_agent.get_response(suggestion)
        print("Their response is " + str(self.next_agent.get_response(suggestion)) + ".")
        # Update the knowledge of the agents based on the suggestion and response
        self.update_knowledge(suggestion, response)
        # Check if there is a winner
        self.model.check_end_state()

    def pick_suggestion(self):
        if RANDOM:
            suggestion = sorted([self.cards.get_random_weapon()] + [self.cards.get_random_suspect()], key=str.lower)
        elif NOT_OWN:
            suggestion = self.pick_other_cards()
        elif ONE_OWN:
            suggestion = self.pick_one_other_card()
        elif ELIMINATING:
            suggestion = self.pick_eliminating_suggestion()
        return suggestion

    def pick_other_cards(self):
        possible_weapon = [weapon for weapon in self.cards.get_all_weapon_cards() if weapon not in self.agent_cards]
        possible_suspect = [suspect for suspect in self.cards.get_all_suspect_cards() if suspect not in self.agent_cards]
        suggestion = sorted([random.choice(possible_weapon)] + [random.choice(possible_suspect)], key=str.lower)
        return suggestion

    def pick_one_other_card(self):
        own_card = random.choice(self.agent_cards)
        if own_card in self.cards.get_all_weapon_cards():
            other_card = random.choice(self.cards.get_all_suspect_cards())
        elif own_card in self.cards.get_all_suspect_cards():
            other_card = random.choice(self.cards.get_all_weapon_cards())
        return sorted([own_card, other_card], key = str.lower)

    # TODO implement (now random)
    def pick_eliminating_suggestion(self):
        return sorted([self.cards.get_random_weapon()] + [self.cards.get_random_suspect()], key=str.lower)

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
            self.next_agent.privately_announce(self, response)

    # Announce privately to the suggesting agents that this agent has a certain card
    def privately_announce(self, suggesting_agent, response):
        # Delete all relations where this agent does not have that card
        for card_1 in self.model.get_cards().get_all_cards():
            if (card_1 == response):
                break
            for card_2 in self.model.get_cards().get_all_cards():
                if (card_2 == response):
                    break
                # For the suggesting agent, remove the relations
                announcement = Not(Atom(str(self.unique_id) + ":" + str(sorted([card_1, card_2], key=str.lower))))
                self.model.get_kripke_model().get_kripke_structure().relation_solve(suggesting_agent, announcement)
