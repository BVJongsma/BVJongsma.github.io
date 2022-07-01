import tkinter as tk
from tkinter import ttk
import Implementation.src.cards as ca
import main


def init_table(num_agents, num_cards):
    win = tk.Tk()
    # title
    win.title('A model of Clue')
    # dimensions
    dim = str(num_agents * 150 + 150) + "x" + str(num_cards * 25 + 50)
    win.geometry(dim)
    # background color
    win['bg'] = '#d61e1e'
    return win


class GameInterface:
    def __init__(self, model):
        self.model = model
        self.num_agents = model.num_agents
        cards_set = ca.Cards(self.num_agents, self.model.num_weapons, self.model.num_suspects)
        self.num_cards = len(cards_set.get_all_cards())
        self.win = init_table(self.num_agents, self.num_cards)
        self.last_agent = -1
        self.finished = False
        # start tree
        columns = ('items',)
        for i in range(1, self.num_agents + 1):
            columns += ('agent' + str(i),)
        self.tree = ttk.Treeview(self.win, column=columns, show='headings', height=(self.num_cards + 1))
        self.KB, self.unknown_cards = self.model.kripke_model.initialise_known_dictionary(self.model.agents)
        self.tree.pack()
        self.init_table_information()
        self.input_KB_table(True)
        self.win.mainloop()

    def update_table(self):
        if self.finished is True:
            print("the winner is already known!")
            return
        # the model takes one agent's turn
        self.last_agent += 1
        self.last_agent %= len(self.model.agents)
        x = self.model.get_agents()[self.last_agent]
        x.step()  # KB is updated during the step
        self.KB, self.unknown_cards = self.model.knowledge_dict, self.model.unknown_cards
        self.input_KB_table(False)  # put KB knowledge in the table
        if self.finished is True:
            main.loop_strategies()

    def refresh_button(self):
        refresh_button = tk.Button(self.win, text="Next Agent's turn", command=self.update_table)
        refresh_button.pack()

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
        card = ca.Cards(3, self.model.num_weapons, self.model.num_suspects)
        cards = card.get_all_cards()
        question = tuple()
        for i in range(self.num_agents):
            question += ('?',)
        data = [(x,) + question for x in cards]
        # including relations
        values = self.get_new_relations()

        # put relations in the table
        self.tree.insert('', tk.END, values=values, iid='relations')
        # put card data in the table
        for d, c in zip(data, cards):
            # for access, use tree.item(iid)['values']
            self.tree.insert('', tk.END, values=d, iid=c)

        # add an update button
        self.refresh_button()
        self.tree.pack()

        return

    #   TODO: make this prettier
    def input_KB_table(self, init):

        if init:
            # list of agents
            agents = self.model.agents

            # list of cards per agents, cards[x] -> the list of cards of agent x
            cards = []
            for i in range(len(agents)):
                cards.append(agents[i].get_agent_cards())

            agents = [a.get_unique_id() for a in self.model.agents]

            # insert info in the table
            for agent in agents:
                for card_name in self.KB[agent - 1]:
                    for c in cards[agent - 1]:
                        if c == card_name:
                            new_tuple = self.tree.item(card_name)['values']
                            new_tuple[agent] = 'Agent ' + str(agent)
                            new_tuple = tuple(new_tuple)
                            self.tree.item(card_name, values=new_tuple)
        elif not init:
            for agent in [a.get_unique_id() for a in self.model.agents]:
                self.tree.item('relations', values=self.get_new_relations())
                env = 0
                for card_name in self.KB[agent - 1]:
                    new_tuple = self.tree.item(card_name)['values']
                    a = self.KB[agent - 1][card_name]
                    if a is None:
                        new_tuple[agent] = '?'
                    elif a == 0:
                        new_tuple[agent] = 'Envelope'
                        env += 1
                    elif a >= 1:
                        new_tuple[agent] = 'Agent ' + str(a)
                    new_tuple = tuple(new_tuple)
                    self.tree.item(card_name, values=new_tuple)
                if env >= 2:
                    self.finished = True

        return

    def get_new_relations(self):
        x = self.model.kripke_model.relations
        values = ('relations',)
        for a in self.model.agents:
            values += (str(len(x[str(a.get_unique_id())])),)
        return values

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
