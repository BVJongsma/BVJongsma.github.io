import random

class Cards():
    def __init__(self, num_agents):
        self.num_agents = num_agents
        self.weapons = ["revolver", "dagger", "rope", "wrench"]
        self.suspects = ["Scarlet", "Mustard", "White", "Plum"]
        self.all_cards = self.weapons + self.suspects
        self.available_cards = self.weapons + self.suspects

    def get_all_cards(self):
        return self.all_cards

    def 

    def get_envelope_weapon(self):
        envelope_weapon = random.choice(self.weapons)
        self.available_cards.remove(envelope_weapon)
        return envelope_weapon

    def get_envelope_suspect(self):
        envelope_suspect = random.choice(self.suspects)
        self.available_cards.remove(envelope_suspect)
        return envelope_suspect

    def get_agent_cards(self):
        num_cards = int(len(self.all_cards) / self.num_agents)
        agent_cards = random.sample(self.available_cards, num_cards)
        self.available_cards = [card for card in self.available_cards if card not in agent_cards]
        return agent_cards
