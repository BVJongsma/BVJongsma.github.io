# From https://github.com/erohkohl/mlsolver

""" Three wise men puzzle

Module contains data model for three wise men puzzle as Kripke strukture and agents announcements as modal logic
formulas
"""
import ast
import copy
import itertools

import numpy as np
import re

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

        print("NUMBER OF WORLDS:")
        print(len(self.worlds))

        self.relations = self.initialise_relations()

        # Add symmetric relations
        self.relations.update(add_symmetric_edges(self.relations))

        print("NUMBER OF RELATIONS PER PLAYER:")
        print(len(self.relations['1']))
        print(len(self.relations['2']))
        print(len(self.relations['3']))
        print("//////////////////////////////")

        # print(len(set(self.relations['2'])))
        # for relation in self.relations:
        #     for connection in self.relations[relation]:
        #         print("\n\n")
        #         print(relation)
        #         print(str(connection[0]))
        #         print("and")
        #         print(str(connection[1]))
        #         print("\n\n")

        self.ks = KripkeStructure(self.worlds, self.relations)

        # TODO add rules
        # If player 1 has card Scarlet themselves, and player 3 says they have one of
        # [Scarlet, wrench], then player 1 knows player 3 has wrench
        # t
        # Delete all where none of them are the case
        # Delete all with reasoning

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
                range_cards = range(len(remaining_cards_list))
                cards_per_player = int(len(remaining_cards_list) / 3)
                worlds, cnt = self.make_kripke_states_players(range_cards, remaining_cards_list, worlds, envelope, cnt,
                                                              cards_per_player)
        return worlds

    # Initialise the relations between the worlds
    def initialise_relations(self):
        relations = {}
        for agent in range(1, self.num_agents + 1):
            relations[str(agent)] = set()
            for i in range(len(self.worlds)):
                for j in range(i, len(self.worlds)):
                    if list(self.worlds[i].assignment.keys())[agent] == list(self.worlds[j].assignment.keys())[agent]:
                        relations[str(agent)].add((self.worlds[i].name, self.worlds[j].name))
        return relations

    # After adding cards to the envelope, create all possible combinations of dividing the cards among the players.
    def make_kripke_states_players(self, indices, cards, worlds, envelope, cnt, cards_per_player):
        # Loop over all possible combinations of two cards out of all remaining cards using their indices.
        for item in list(itertools.combinations(indices, cards_per_player)):
            # Add those cards to a temporary world variable, as cards for player 1.
            world_temp = copy.deepcopy(envelope)
            cards_1 = []
            delete_indices = []
            for index in range(cards_per_player):
                cards_1.append(cards[item[index]])
                delete_indices.append(item[index])
            world_temp.append(cards_1)
            # Remove the cards that player 1 has from the remaining cards.
            remaining_cards = cards
            remaining_cards = np.delete(remaining_cards, delete_indices)
            # Loop over all possible combinations of two cards out of all remaining cards using their indices.
            range_cards = range(len(remaining_cards))
            for second_player in list(itertools.combinations(range_cards, cards_per_player)):
                world_cards = {}
                # Add those cards as cards for player 2.
                world = copy.deepcopy(world_temp)
                cards_2 = []
                delete_indices = []
                for index in range(cards_per_player):
                    cards_2.append(remaining_cards[second_player[index]])
                    delete_indices.append(second_player[index])
                world.append(cards_2)
                # Add the remaining cards as cards for player 3.
                remaining_indices = np.delete(range_cards, delete_indices)
                cards_3 = []
                for index in range(cards_per_player):
                    cards_3.append(remaining_cards[remaining_indices[index]])
                world.append(cards_3)
                # Sort the cards per envelope or player alphabetically
                world = self.sort_world(world)
                # Make a dictionary for the cards per envelope or player
                world_cards['env:' + str(world[0])] = True
                world_cards['1:' + str(world[1])] = True
                world_cards['2:' + str(world[2])] = True
                world_cards['3:' + str(world[3])] = True
                # Make sure the world is given in the correct format:
                # World(name, {'env:['card1', 'card2']', '1:['card3', 'card4']', '2:['card5', 'card6']', '3:['card7', 'card8']'})
                world_correct_format = World(str(cnt), world_cards)
                # Add the world to the list of all worlds
                worlds.append(world_correct_format)
                cnt = cnt + 1
        return worlds, cnt

    # Sort the cards within a world (per envelope or player) alphabetically
    def sort_world(self, world):
        new_world = []
        for card_set in world:
            card_set = sorted(card_set, key=str.lower)
            new_world.append(card_set)
        return new_world

    # Find a winner amongst the agents by checking the knowledge of the agents
    def find_winner(self):
        winner = []
        guess = []
        # Go through all agents
        for agent in range(1, self.num_agents + 1):
            old_envelope = None
            cnt = 0
            goal_cnt = len(self.relations[str(agent)])
            # For each agent, find out if every relation has a world that has the same guess for the envelope
            for relation in self.relations[str(agent)]:
                cnt += 1
                relation_world = self.worlds[int(relation[1])]
                envelope = list(relation_world.assignment.keys())[0]
                if old_envelope is None:
                    old_envelope = envelope
                elif envelope != old_envelope:
                    break
            if cnt == goal_cnt:
                winner.append(agent)
                guess.append(envelope)
                break

        return winner, guess

    # Get cards that are unknown for an agent (i.e. could be in the hands of various players/the envelope)
    def get_unknown_cards(self, cards, agent_id):
        unknown_cards = []
        # Go through all cards
        for card in cards:
            old_i = None
            unknown = False
            # For each card, keep track of where they belong according to the worlds
            for relation in self.relations[str(agent_id)]:
                relation_world = self.worlds[int(relation[1])]
                # i is the envelope (0), or one of the agents (1, 2 or 3)
                for i in range(self.num_agents):
                    # Turn the strings in a world assignment to a list
                    i_cards = re.findall(r'\:(.*)', str(list(relation_world.assignment.keys())[i]))[0]
                    i_cards_list = ast.literal_eval(i_cards)
                    i_cards_list = [i_card.strip() for i_card in i_cards_list]
                    if card in i_cards_list:
                        new_i = i
                        if old_i == None:
                            old_i = new_i
                        elif new_i != old_i:
                            print(new_i)
                            print(old_i)
                            unknown_cards.append(card)
                            unknown = True
                            break
                        else:
                            old_i = new_i
                if unknown:
                    break
        return unknown_cards


def add_symmetric_edges(relations):
    """Routine adds symmetric edges to Kripke frame
    """
    result = {}
    for agent, agents_relations in relations.items():
        result_agents = agents_relations.copy()
        for r in agents_relations:
            x, y = r[1], r[0]
            result_agents.add((x, y))
        result[agent] = result_agents
    return result
