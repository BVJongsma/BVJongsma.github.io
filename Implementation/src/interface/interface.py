import tkinter as tk
from tkinter import ttk
import Implementation.src.cards as ca
import Implementation.src.clue_agent
import Implementation.src.clue_model as cm

""""
:returns
    agents: a list of int, where the int are the agent id's
    cards: a list of lists of cards. cards[id] returns the list of cards that agent 'id' owns.
    unknown_cards: a list of list of cards. unknown_cards[id] returns a list of cards that agent 'id' still
            doesn't know where they are yet.
    dictionary: a list of dictionary summarising what all the agents know. dictionary[id] returns a dictionary of agent 'id'.
            dictionary[x][y] = list shows what agent x knows about card y.
            e.g. dictionary[1] = {'candle': [], ....}-> a dictionary showing where each card is in knowledge of agent 1 
            e.g. dictionary[1]['dagger'] = 2 -> agent 1 knows that agent 2 has the dagger.        
"""


def fake_data():
    agents = [1, 2, 3]
    all_cards = ['candle', 'dagger', 'rope', 'wrench'] + ["Green", "Mustard", "Plum", "Scarlet"]
    empty_dict = {i: [] for i in all_cards}
    agent1_cards = ['candle', 'dagger']
    agent1_unknown = list(set(all_cards) - set(agent1_cards))
    # agent1_dict = {1: agent1_cards, 2: [], 3: [], 'env': []}
    agent1_dict = empty_dict.copy()
    for i in agent1_cards:
        agent1_dict[i] = 1
    # print("agent 1 dictionary: ", agent1_dict)
    agent2_cards = ['wrench', 'Mustard']
    agent2_unknown = list(set(all_cards) - set(agent2_cards))
    # agent2_dict = {1: [], 2: agent2_cards, 3: [], 'env': []}
    agent2_dict = empty_dict.copy()
    for i in agent2_cards:
        agent2_dict[i] = 2
    # print("agent 2 dictionary: ", agent2_dict)
    agent3_cards = ['Plum', 'Scarlet']
    agent3_unknown = list(set(all_cards) - set(agent3_cards))
    # agent3_dict = {1: [], 2: [], 3: agent3_cards, 'env': []}
    agent3_dict = empty_dict.copy()
    for i in agent3_cards:
        agent3_dict[i] = 3
    # print("agent 3 dictionary: ", agent3_dict)
    # env_cards = ['Green', 'rope']
    cards = [agent1_cards, agent2_cards, agent3_cards]
    unknown_cards = [agent1_unknown, agent2_unknown, agent3_unknown]
    dictionary = [agent1_dict, agent2_dict, agent3_dict]
    return agents, cards, unknown_cards, dictionary


def init_table(num_agents, num_cards):
    win = tk.Tk()
    # title
    win.title('A model of Clue')
    # dimensions
    dim = str(num_agents * 150 + 150) + "x" + str(num_cards * 25 + 25)
    win.geometry(dim)
    # background color
    win['bg'] = '#d61e1e'
    return win


class GameInterface:
    def __init__(self, model):
        self.model = model
        self.num_agents = model.num_agents
        cards_set = ca.Cards(self.num_agents)
        self.num_cards = len(cards_set.get_all_cards())
        self.win = init_table(self.num_agents, self.num_cards)
        self.last_agent = -1
        # start tree
        columns = ('items',)
        for i in range(1, self.num_agents + 1):
            columns += ('agent' + str(i),)
        self.tree = ttk.Treeview(self.win, column=columns, show='headings', height=self.num_cards)
        self.KB = self.init_KB()
        self.tree.pack()
        self.init_table_information()
        self.input_KB_table()
        self.win.mainloop()

    def update_table(self):
        # the model takes one agent's turn
        self.last_agent += 1
        self.last_agent %= len(self.model.agents)
        x = self.model.get_agents()[self.last_agent]
        x.step()
        #if you first do this using the interface and then escape and do it using pressing enter, you potentially skip an agent
        #TODO: fix this

        #KB is updated and then put in the table
        self.update_KB()
        self.input_KB_table()



    """
    initialise the knowledge base. This includes all the agents own cards.
    :return
        KB -> list of dictionaries.
        KB[id] -> a dictionary, this is the knowledge base of agent x.
        KB[id][card] -> a list of integers, containing the id's of the agents that agent id believes own the card.
    """
    def init_KB(self):
        empty_dict = {i: [] for i in self.model.cards.get_all_cards()}
        KB = [empty_dict.copy()]
        for a in self.model.envelope.get_envelope_cards():
            KB[0][a] = 'env'
        for a in self.model.agents:
            KB.append(empty_dict.copy())
            for i in a.get_agent_cards():
                KB[a.get_unique_id()][i] = a.get_unique_id()
        print(KB)
        return KB

    # TODO: implement this
    def update_KB(self):

        #unknown_cards -= new_known_cards
        return

    def refresh_button(self):
        refresh_button = tk.Button(self.win, text="Next Agent's turn", command=self.update_table)
        refresh_button.pack()

    #TODO: put in extra row with amount of relations?

    def init_table_information(self):
        # define columns and headings
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.heading("#0", text="", anchor=tk.CENTER)
        self.tree.column('items', anchor=tk.CENTER, width=150)
        self.tree.heading('items', text='Items')
        # make the agent columns & headings
        for i in range(1, self.num_agents + 1):
            self.tree.column('agent' + str(i), anchor=tk.CENTER, width=150)
            self.tree.heading('agent' + str(i), text='Agent ' + str(i))

        # generate list of data to put in the table
        card = ca.Cards(3)
        cards = card.get_all_cards()
        question = tuple()
        for i in range(self.num_agents):
            question += ('?',)
        data = [(x,) + question for x in cards]

        # put data in the table
        for d, c in zip(data, cards):
            # for access, use tree.item(iid)['values']
            self.tree.insert('', tk.END, values=d,
                             iid=c)  # tk.END means add at the end of the list, '0' means add at the beginning

        # add an update button
        self.refresh_button()
        self.tree.pack()

        return

    def input_KB_table(self):
        # list of agents
        agents = self.model.agents

        # list of cards per agents, cards[x] -> the list of cards of agent x
        cards = []
        for i in range(len(agents)):
            cards.append(agents[i].get_agent_cards())

        agents = [a.get_unique_id() for a in self.model.agents]

        # insert info in the table
        for agent in agents:
            for card_info in self.KB[agent]:
                for c in cards[agent - 1]:
                    if c == card_info:
                        new_tuple = self.tree.item(c)['values']
                        new_tuple[agent] = 'Agent ' + str(agent)
                        new_tuple = tuple(new_tuple)
                        self.tree.item(c, values=new_tuple)
        return

    def get_model(self):
        return self.model

    def get_num_agents(self):
        return self.num_agents

    def get_win(self):
        return self.win

    def get_tree(self):
        return self.tree

# agents, cards, unknown, dict = fake_data()
# print(dict)
