# This is a pseudocode idea of how we want to set up the model.
__authors__ = "Bonne Jongsma", "Naomï Broersma", "Iris Kamsteeg"

from Implementation.Pseudocode import cards
import model

def distribute_cards():
    all_cards = cards.Card.initiate_cards()
    envelope = "Revolver", "Scarlet"
    a1 = "Rope", "Dagger"
    a2 = "White", "Plum"
    a3 = "Wrench", "Mustard"
    return



def nobody_knows(model):
    #an agent knows the contents of the envelope if
    # the envelope contains the same cards in all states accessible to an agent.
    # This is checked in this
    return True

def question(a1, a2, model):
    # a1 asks a question to a2 and gets a response.
    return True

def pseudocode():
    a1, a2, a3, env = distribute_cards() #distribute the n cards over the players and the envelope.
    m = model.initiate_states() #set up the model with all the states possible
    m = model.initiate_relations(m, a1, a2, a3, env) #set up the relations
    m = model.update_states(m, False)
    for agent1 in a1,a2,a3, agent2 in a2,a3,a1:
        while nobody_knows(m): #taking turns untill an agent knows the answer.
            information = question(agent1, agent2, model)
            m = model.update_relations(m, information) #relations are changed.
            m = model.update_states(m) #erase states with no accessibility relations
    winner =
    return winner


if __name__ == '__main__':
    pseudocode()
    print('This is a model of Clue.')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
