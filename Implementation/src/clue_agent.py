import random
import mesa
from Implementation.src.mlsolver.formula import Atom

PRINT = True

class ClueAgent(mesa.Agent):
    """An agent who plays the game of Clue."""

    # Initialise the agent.
    def __init__(self, unique_id, cards, agent_cards, strategy, model, response_strategy):
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.cards = cards
        self.agent_cards = agent_cards
        self.model = model
        self.next_agent = None
        self.strategy = strategy
        self.cards_shown = []
        self.response_strategy = response_strategy

    # Set the agent that is next in turn and that a suggestion is made to
    def initialise_next_agent(self):
        next_agent_id = self.unique_id + 1
        if next_agent_id > self.model.get_num_agents():
            next_agent_id = 1
        self.next_agent = self.model.get_agent_from_id(next_agent_id)

    # Get the current agent's ID.
    def get_unique_id(self):
        return self.unique_id

    # Get the cards of the agent.
    def get_agent_cards(self):
        return self.agent_cards

    # Get a response of the current agent based on the suggestion that is made
    def get_response(self, suggestion):
        possible_response_cards = list(set(self.agent_cards).intersection(suggestion))
        # If the agent has none of the cards asked, respond with None.
        if len(possible_response_cards) < 1:
            response_card = None
        else:
            # Randomly select one of the possible cards to respond.
            if self.response_strategy == "RANDOM":
                response_card = random.choice(possible_response_cards)
                self.cards_shown.append(response_card)
            else:  # response_strategy == "SHOWN"
                response_card = random.choice(possible_response_cards)
                # If a card is in the list of cards shown, select that card and show it.
                for card in possible_response_cards:
                    if card in self.cards_shown:
                        response_card = card
                # If none of the cards were shown yet, add the response card to the list of shown cards.
                if response_card not in self.cards_shown:
                    self.cards_shown.append(response_card)
        return response_card

    # Take a turn
    def step(self):
        # The agent takes a turn if the winner has not been determined yet.
        if not self.model.check_end_state():
            # Let the current agent make a suggestion
            suggestion = self.pick_suggestion()
            # Get a response from the next agent on whether they have any of the cards
            response = self.next_agent.get_response(suggestion)
            if PRINT:
                print("This is agent " + str(self.unique_id) + ".")
                print("With cards " + str(self.agent_cards) + ".")
                print("They suggest " + str(suggestion) + ".")
                print("The agent they suggest to is agent " + str(self.next_agent.get_unique_id()) + ".")
                print("Their response is " + str(response) + ".")
            # Update the knowledge of the agents based on the suggestion and response
            self.update_knowledge(suggestion, response)
        else:
            suggestion = []
            response = ""
        return suggestion, response

    # Pick a suggestion, based on the strategy of the agent.
    def pick_suggestion(self):
        # Pick random suggestion
        if self.strategy == "RANDOM":
            suggestion = sorted([self.cards.get_random_weapon()] + [self.cards.get_random_suspect()], key=str.lower)
        # Pick two cards that the agent does not have themselves
        elif self.strategy == "NOT_OWN":
            suggestion = self.pick_other_cards()
        # Pick one card that the agent has themselves and another that the agent does not have themselves
        elif self.strategy == "ONE_OWN":
            suggestion = self.pick_one_other_card()
        # Pick two cards for which the agent does not know to whom they belong
        elif self.strategy == "UNKNOWN":
            suggestion = self.pick_unknown_cards()
        # Pick one card that the agent knows about and one unknown card
        elif self.strategy == "ONE_UNKNOWN":
            suggestion = self.pick_one_unknown_card()
        # Pick one card that the agent knows about and isn't of the next agent, and one card that might be of the next
        # agent or in the envelope (or if there are none such cards: that might be of the next agent)
        elif self.strategy == "REASONING":
            suggestion = self.pick_reasoning_suggestion()
        return suggestion

    # Pick two cards that the agent does not have themselves
    def pick_other_cards(self):
        possible_weapon = [weapon for weapon in self.cards.get_all_weapon_cards() if weapon not in self.agent_cards]
        possible_suspect = [suspect for suspect in self.cards.get_all_suspect_cards() if
                            suspect not in self.agent_cards]
        # Randomly select one of the weapon cards the agent does not have and one of the suspect cards
        # the agent does not have.
        suggestion = sorted([random.choice(possible_weapon)] + [random.choice(possible_suspect)], key=str.lower)
        return suggestion

    # Pick one card that the agent has themselves and another that the agent does not have themselves
    def pick_one_other_card(self):
        # Randomly select a card the agent has.
        own_card = random.choice(self.agent_cards)
        # If the selected card is a weapon, select a random suspect card.
        if own_card in self.cards.get_all_weapon_cards():
            other_card = random.choice(self.cards.get_all_suspect_cards())
            # If the selected card is a suspect, select a random weapon card.
        elif own_card in self.cards.get_all_suspect_cards():
            other_card = random.choice(self.cards.get_all_weapon_cards())
        return sorted([own_card, other_card], key=str.lower)

    # Pick two cards for which the agent does not know to whom they belong
    def pick_unknown_cards(self):
        # Create a list of weapons for which the agent does not know where they are.
        unknown_weapons = list(
            set(self.model.get_unknown_cards(self.unique_id - 1)).intersection(self.cards.get_all_weapon_cards()))
        # If there are no unknown weapons, select a random one.
        if not unknown_weapons:
            unknown_weapons.append(random.choice(self.cards.get_all_weapon_cards()))
        # Create a list of suspect for which the agent does not know where they are.
        unknown_suspects = list(
            set(self.model.get_unknown_cards(self.unique_id - 1)).intersection(self.cards.get_all_suspect_cards()))
        # If there are no unknown suspects, select a random one.
        if not unknown_suspects:
            unknown_suspects.append(random.choice(self.cards.get_all_suspect_cards()))
        # Return a random unknown weapon and suspect.
        return sorted([random.choice(unknown_weapons), random.choice(unknown_suspects)], key=str.lower)

    # Pick one card that the agent knows about and one unknown card
    def pick_one_unknown_card(self):
        # First, pick an unknown card
        unknown_cards = self.model.get_unknown_cards(self.unique_id - 1)
        unknown_weapons = list(set(self.cards.get_all_weapon_cards()).intersection(unknown_cards))
        unknown_suspects = list(set(self.cards.get_all_suspect_cards()).intersection(unknown_cards))
        # No known cards that are weapons, so select an unknown weapon
        if len(unknown_weapons) == len(self.cards.get_all_weapon_cards()):
            unknown_card = random.choice(unknown_weapons)
            # No known cards that are suspects, so select an unknown suspect
        elif len(unknown_suspects) == len(self.cards.get_all_suspect_cards()):
            unknown_card = random.choice(unknown_suspects)
            # Else, select a random unknown card
        else:
            unknown_card = random.choice(unknown_cards)
        # Second, pick a known card
        known_cards = set(self.cards.get_all_cards()).difference(set(unknown_cards))
        known_weapons = list(set(self.cards.get_all_weapon_cards()).intersection(known_cards))
        known_suspects = list(set(self.cards.get_all_suspect_cards()).intersection(known_cards))
        # If the unknown card is a weapon, select a known suspect.
        if unknown_card in self.cards.get_all_weapon_cards():
            known_card = random.choice(known_suspects)
        else:
            # Else, select a known weapon
            known_card = random.choice(known_weapons)
        return sorted([unknown_card, known_card], key=str.lower)

    # Actually pick the cards for the reasoning suggestion approach.
    def pick_cards_reasoning_suggestion(self, possible_cards, known_cards):
        # The lists of unknown and known weapons and suspsects.
        unknown_weapons = list(set(self.cards.get_all_weapon_cards()).intersection(possible_cards))
        unknown_suspects = list(set(self.cards.get_all_suspect_cards()).intersection(possible_cards))

        known_weapons = list(set(self.cards.get_all_weapon_cards()).intersection(known_cards))
        known_suspects = list(set(self.cards.get_all_suspect_cards()).intersection(known_cards))

        # If all of those lists are not empty
        if known_weapons and known_suspects and unknown_weapons and unknown_suspects:
            # Select a random unknown card and a random known card from the other category.
            unknown_card = random.choice(possible_cards)
            if unknown_card in unknown_weapons:
                known_card = random.choice(known_suspects)
            else:
                known_card = random.choice(known_weapons)
        # If the known weapons and unknown suspects are not empty, select a random one of those.
        elif known_weapons and unknown_suspects:
            known_card = random.choice(known_weapons)
            unknown_card = random.choice(unknown_suspects)
        # If the known suspects and unknown weapons are not empty, select a random one of those.
        elif known_suspects and unknown_weapons:
            known_card = random.choice(known_suspects)
            unknown_card = random.choice(unknown_weapons)
        # Else, set known and unknown card to None.
        else:
            known_card = None
            unknown_card = None

        return known_card, unknown_card

    # Pick one card that the agent knows about and isn't of the next agent, and one card that might be of the next
    # agent or in the envelope (or if there are none such cards: that might be of the next agent)
    def pick_reasoning_suggestion(self):
        # Pick one card that might be of the next agent or in the envelope, but is currently unknown
        unknown_cards = self.model.get_unknown_cards(self.unique_id - 1)
        possible_envelope_cards, possible_next_agent_cards = self.model.get_kripke_model().find_possible_cards(
            unknown_cards, self.unique_id, self.next_agent.get_unique_id())

        # Possible cards is the list of cards that might be in the envelope or belong to the next agent.
        possible_cards = list(set(possible_envelope_cards).intersection(set(possible_next_agent_cards)))

        # Pick one card that the agent knows about and isn't of the next agent
        known_cards = set(self.cards.get_all_cards()).difference(set(unknown_cards))
        agent_knowledge_dict = self.model.get_knowledge_dict()[self.unique_id - 1]
        known_cards = [known_card for known_card in known_cards if
                       (agent_knowledge_dict[known_card] != self.next_agent.get_unique_id())]

        # If there are no unknown cards that might be in the envelope or belong to the next agent, use the cards
        # that might belong to the next agent.
        if not possible_cards:
            known_card, unknown_card = self.pick_cards_reasoning_suggestion(possible_next_agent_cards, known_cards)
        else:
            # Use the cards that could be in envelope or belong to next agent.
            known_card, unknown_card = self.pick_cards_reasoning_suggestion(possible_cards, known_cards)
            # If there is no known card, use only the cards that could belong to the next agent.
            if known_card is None:
                known_card, unknown_card = self.pick_cards_reasoning_suggestion(possible_next_agent_cards, known_cards)

        # If there is no known card, randomly select a card.
        if known_card is None:
            known_card = self.cards.get_random_weapon()
            unknown_card = self.cards.get_random_suspect()

        return sorted([known_card, unknown_card], key=str.lower)

    # Update the knowledge of all agents via a public or private announcement
    def update_knowledge(self, suggestion, response):
        if response is None:  # Next agent does not have any of the cards
            # Publicly announce that next agent does not have any
            self.model.publicly_announce(self, self.next_agent, suggestion, False)
        else:  # Next agent does have one of the cards
            # Publicly announce that next agent does have one
            self.model.publicly_announce(self, self.next_agent, suggestion, True)
            # Privately announce the card of next agent to this self agent
            self.privately_announce(response)
        self.model.update_knowledge_dict()

    # Announce privately to the suggesting agents that this agent has a certain card
    def privately_announce(self, response):
        announcement = Atom(response)
        if PRINT:
            print("private announcement", announcement)
        asked_agent_id = self.next_agent.get_unique_id()
        # Update the relations for the agent that asked for the cards.
        self.model.kripke_model.get_kripke_structure().relation_solve(self, announcement, asked_agent_id)
