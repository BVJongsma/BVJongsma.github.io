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


class WiseMenWithHat:
    """
    Class models the Kripke structure of the "Three wise men example.
    """

    knowledge_base = []

    def __init__(self):
        worlds = [
            World('RWW', {'1:R': True, '2:W': True, '3:W': True}),
            World('RRW', {'1:R': True, '2:R': True, '3:W': True}),
            World('RRR', {'1:R': True, '2:R': True, '3:R': True}),
            World('WRR', {'1:W': True, '2:R': True, '3:R': True}),

            World('WWR', {'1:W': True, '2:W': True, '3:R': True}),
            World('RWR', {'1:R': True, '2:W': True, '3:R': True}),
            World('WRW', {'1:W': True, '2:R': True, '3:W': True}),
            World('WWW', {'1:W': True, '2:W': True, '3:W': True}),
        ]

        relations = {
            '1': {('RWW', 'WWW'), ('RRW', 'WRW'), ('RWR', 'WWR'), ('WRR', 'RRR')},
            '2': {('RWR', 'RRR'), ('RWW', 'RRW'), ('WRR', 'WWR'), ('WWW', 'WRW')},
            '3': {('WWR', 'WWW'), ('RRR', 'RRW'), ('RWW', 'RWR'), ('WRW', 'WRR')}
        }

        relations.update(add_reflexive_edges(worlds, relations))
        relations.update(add_symmetric_edges(relations))

        self.ks = KripkeStructure(worlds, relations)

        # Wise man ONE does not know whether he wears a red hat or not
        self.knowledge_base.append(And(Not(Box_a('1', Atom('1:R'))), Not(Box_a('1', Not(Atom('1:R'))))))

        # This announcement implies that either second or third wise man wears a red hat.
        self.knowledge_base.append(Box_star(Or(Atom('2:R'), Atom('3:R'))))

        # Wise man TWO does not know whether he wears a red hat or not
        self.knowledge_base.append(And(Not(Box_a('2', Atom('2:R'))), Not(Box_a('2', Not(Atom('2:R'))))))

        # This announcement implies that third men has be the one, who wears a red hat
        self.knowledge_base.append(Box_a('3', Atom('3:R')))


class Clue:
    """
    Class models the Kripke structure of Clue.
    """

    knowledge_base = []

    def __init__(self, cards):
        print(cards.get_all_cards())
        worlds = self.initialise_worlds(cards)
        relations = self.initialise_relations()

        # TODO do we add reflexive and symmetric edges?
        relations.update(add_reflexive_edges(worlds, relations))
        relations.update(add_symmetric_edges(relations))

        self.ks = KripkeStructure(worlds, relations)

    def initialise_worlds(self, cards):
        # TODO create worlds
        self.all_different_combinations_envelope(cards)
        worlds = [
            World('RWW', {'1:R': True, '2:W': True, '3:W': True}),
            World('RRW', {'1:R': True, '2:R': True, '3:W': True}),
            World('RRR', {'1:R': True, '2:R': True, '3:R': True}),
            World('WRR', {'1:W': True, '2:R': True, '3:R': True}),

            World('WWR', {'1:W': True, '2:W': True, '3:R': True}),
            World('RWR', {'1:R': True, '2:W': True, '3:R': True}),
            World('WRW', {'1:W': True, '2:R': True, '3:W': True}),
            World('WWW', {'1:W': True, '2:W': True, '3:W': True}),
        ]
        return worlds

    def initialise_relations(self):
        # TODO create relations
        relations = {
            '1': {('RWW', 'WWW'), ('RRW', 'WRW'), ('RWR', 'WWR'), ('WRR', 'RRR')},
            '2': {('RWR', 'RRR'), ('RWW', 'RRW'), ('WRR', 'WWR'), ('WWW', 'WRW')},
            '3': {('WWR', 'WWW'), ('RRR', 'RRW'), ('RWW', 'RWR'), ('WRW', 'WRR')}
        }
        return relations

    # TODO make more general
    def all_different_combinations_envelope(self, cards):
        cards_list = cards.get_all_cards()
        weapons_list = cards.get_all_weapon_cards()
        suspects_list = cards.get_all_suspect_cards()
        worlds = []
        for weapon in weapons_list:
            for suspect in suspects_list:
                envelope = [[weapon, suspect]]
                remaining_cards_list = copy.deepcopy(cards_list)
                remaining_cards_list.remove(weapon)
                remaining_cards_list.remove(suspect)
                worlds = self.make_kripke_states_players(range(6), remaining_cards_list, worlds, envelope)
                break

        pass

    # TODO make more general by replacing 2, range(4) and item[0], item[1] references.
    def make_kripke_states_players(self, indices, cards, worlds, envelope):
        for item in list(itertools.combinations(indices, 2)):
            world_temp = copy.deepcopy(envelope)
            world_temp.append([cards[item[0]], cards[item[1]]])
            delete_indices = [item[0], item[1]]
            remaining_cards = cards
            remaining_cards = np.delete(remaining_cards, delete_indices)
            for second_item in list(itertools.combinations(range(4), 2)):
                world = copy.deepcopy(world_temp)
                world.append([remaining_cards[second_item[0]], remaining_cards[second_item[1]]])
                delete_indices = [second_item[0], second_item[1]]
                remaining_indices = np.delete(range(4), delete_indices)
                world.append([remaining_cards[remaining_indices[0]], remaining_cards[remaining_indices[1]]])
                print(world)
                worlds.append(world)
        return worlds


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


def add_reflexive_edges(worlds, relations):
    """Routine adds reflexive edges to Kripke frame
    """
    result = {}
    for agent, agents_relations in relations.items():
        result_agents = agents_relations.copy()
        for world in worlds:
            result_agents.add((world.name, world.name))
            result[agent] = result_agents
    return result
