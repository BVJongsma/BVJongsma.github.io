# From https://github.com/erohkohl/mlsolver

""" Three wise men puzzle

Module contains data model for three wise men puzzle as Kripke strukture and agents announcements as modal logic
formulas
"""
import copy
import itertools

import numpy as np

from Implementation.Code.mlsolver.kripke import KripkeStructure, World
from Implementation.Code.mlsolver.formula import Atom, And, Not, Or, Box_a, Box_star
from Implementation.Code.cards import Cards


#
# class WiseMenWithHat:
#     """
#     Class models the Kripke structure of the "Three wise men example.
#     """
#
#     knowledge_base = []
#
#     def __init__(self):
#         worlds = [
#             World('RWW', {'1:R': True, '2:W': True, '3:W': True}),
#             World('RRW', {'1:R': True, '2:R': True, '3:W': True}),
#             World('RRR', {'1:R': True, '2:R': True, '3:R': True}),
#             World('WRR', {'1:W': True, '2:R': True, '3:R': True}),
#
#             World('WWR', {'1:W': True, '2:W': True, '3:R': True}),
#             World('RWR', {'1:R': True, '2:W': True, '3:R': True}),
#             World('WRW', {'1:W': True, '2:R': True, '3:W': True}),
#             World('WWW', {'1:W': True, '2:W': True, '3:W': True}),
#         ]
#
#         relations = {
#             '1': {('RWW', 'WWW'), ('RRW', 'WRW'), ('RWR', 'WWR'), ('WRR', 'RRR')},
#             '2': {('RWR', 'RRR'), ('RWW', 'RRW'), ('WRR', 'WWR'), ('WWW', 'WRW')},
#             '3': {('WWR', 'WWW'), ('RRR', 'RRW'), ('RWW', 'RWR'), ('WRW', 'WRR')}
#         }
#
#         relations.update(add_reflexive_edges(worlds, relations))
#         relations.update(add_symmetric_edges(relations))
#
#         self.ks = KripkeStructure(worlds, relations)
#
#         # Wise man ONE does not know whether he wears a red hat or not
#         self.knowledge_base.append(And(Not(Box_a('1', Atom('1:R'))), Not(Box_a('1', Not(Atom('1:R'))))))
#
#         # This announcement implies that either second or third wise man wears a red hat.
#         self.knowledge_base.append(Box_star(Or(Atom('2:R'), Atom('3:R'))))
#
#         # Wise man TWO does not know whether he wears a red hat or not
#         self.knowledge_base.append(And(Not(Box_a('2', Atom('2:R'))), Not(Box_a('2', Not(Atom('2:R'))))))
#
#         # This announcement implies that third men has be the one, who wears a red hat
#         self.knowledge_base.append(Box_a('3', Atom('3:R')))


class Clue:
    """
    Class models the Kripke structure of Clue.
    """

    knowledge_base = []

    def __init__(self, cards, num_agents):
        self.num_agents = num_agents
        self.worlds = self.initialise_worlds(cards)
        self.relations = self.initialise_relations()

        # Add symmetric relations
        self.relations.update(add_symmetric_edges(self.relations))

        # for relation in relations:
        #     for connection in relations[relation]:
        #         print("\n\n")
        #         print(relation)
        #         print(str(connection[0]))
        #         print("and")
        #         print(str(connection[1]))
        #         print("\n\n")

        self.ks = KripkeStructure(self.worlds, self.relations)

    # Get the Kripke structure
    def get_kripke_structure(self):
        return self.ks

    # Initialise the worlds that represent the possible states in a game of Clue
    def initialise_worlds(self, cards):
        cards_list = cards.get_all_cards()
        weapons_list = cards.get_all_weapon_cards()
        suspects_list = cards.get_all_suspect_cards()
        worlds = []
        cnt = 0
        # Draw one weapon.
        for weapon in weapons_list:
            # Draw one suspect.
            for suspect in suspects_list:
                # Add the weapon and suspect to the envelope.
                envelope = [[weapon, suspect]]
                # Make a list of the cards that remain after removing the cards in the envelope.
                remaining_cards_list = copy.deepcopy(cards_list)
                remaining_cards_list.remove(weapon)
                remaining_cards_list.remove(suspect)
                # For this combination of cards in the envelope, create all possible worlds.
                worlds, cnt = self.make_kripke_states_players(range(6), remaining_cards_list, worlds, envelope, cnt)
        return worlds

    def initialise_relations(self):
        # TODO create relations
        relations = self.generate_relations()
        return relations

    def generate_relations(self):
        relations = {}
        for agent in range(1, self.num_agents + 1):
            relations[str(agent)] = []
            for i in range(len(self.worlds)):
                for j in range(i, len(self.worlds)):
                    if set(self.worlds[i].assignment[str(agent)]) == set(self.worlds[j].assignment[str(agent)]):
                        relations[str(agent)].append((self.worlds[i], self.worlds[j]))

        print(len(relations))
        print(len(relations['1']))
        print(len(relations['2']))
        print(len(relations['3']))
        return relations

    # TODO make more general by replacing 2, range(4) and item[0], item[1] references.

    # After adding cards to the envelope, create all possible combinations of dividing the cards among the players.
    def make_kripke_states_players(self, indices, cards, worlds, envelope, cnt):
        # Loop over all possible combinations of two cards out of all remaining cards using their indices.
        world_cards = {}
        for item in list(itertools.combinations(indices, 2)):
            # Add those cards to a temporary world variable, as cards for player 1.
            world_temp = copy.deepcopy(envelope)
            world_temp.append([cards[item[0]], cards[item[1]]])
            # Remove the cards that player 1 has from the remaining cards.
            delete_indices = [item[0], item[1]]
            remaining_cards = cards
            remaining_cards = np.delete(remaining_cards, delete_indices)
            # Loop over all possible combinations of two cards out of all remaining cards using their indices.
            for second_item in list(itertools.combinations(range(4), 2)):
                # Add those cards as cards for player 2.
                world = copy.deepcopy(world_temp)
                world.append([remaining_cards[second_item[0]], remaining_cards[second_item[1]]])
                delete_indices = [second_item[0], second_item[1]]
                # Add the remaining cards as cards for player 3.
                remaining_indices = np.delete(range(4), delete_indices)
                world.append([remaining_cards[remaining_indices[0]], remaining_cards[remaining_indices[1]]])
                # Sort the cards per envelope or player alphabetically
                world = self.sort_world(world)
                # Make a dictionary for the cards per envelope or player
                world_cards['env'] = world[0]
                world_cards['1'] = world[1]
                world_cards['2'] = world[2]
                world_cards['3'] = world[3]
                # Make sure the world is given in the correct format:
                # World(name, {'env' : [cards envelope], '1' : [cards player 1], '2' : [cards player 2], '3' : [cards player 3]})
                world_correct_format = World(str(cnt), world_cards)
                # Add the world to the list of all worlds
                worlds.append(world_correct_format)
                cnt = cnt + 1
        return worlds, cnt

    # Sort the cards within a world (per envelope or player) alphabetically
    def sort_world(self, world):
        new_world = []
        for card_set in world:
            card_set = sorted(card_set, key = str.lower)
            new_world.append(card_set)
        return new_world

def add_symmetric_edges(relations):
    """Routine adds symmetric edges to Kripke frame
    """
    result = {}
    for agent, agents_relations in relations.items():
        result_agents = agents_relations.copy()
        for r in agents_relations:
            x, y = r[1], r[0]
            result_agents.append((x, y))
        result[agent] = result_agents
    return result
