import tkinter as tk
from tkinter import ttk
import Implementation.src.cards as ca
import main

class GameInterface:
    """"
    The interface of the game: this shows a table displaying what information each agent has.

    """
    def __init__(self, model):
        self.model = model
        self.num_agents = model.num_agents
        cards_set = ca.Cards(self.num_agents, self.model.num_weapons, self.model.num_suspects)
        self.num_cards = len(cards_set.get_all_cards())
        self.win = init_window(self.num_agents, self.num_cards)
        self.last_agent = -1
        self.finished = False
        self.winner = []
        columns = ('items',)
        for i in range(1, self.num_agents + 1):
            columns += ('agent' + str(i),)
        self.tree = ttk.Treeview(self.win, column=columns, show='headings', height=(self.num_cards + 1))
        self.KB, self.unknown_cards = self.model.kripke_model.initialise_known_dictionary(self.model.agents)
        self.tree.pack()
        self.init_table_information()
        self.input_KB_table()
        self.refresh_button()
        self.canvas, self.line1, self.line2 = self.message_frame_init()
        self.win.mainloop()

    def message_frame_init(self):
        frame = tk.Frame()
        frame.pack(pady=5)
        WIDTH=450
        HEIGHT=75
        canvas = tk.Canvas(self.win, width=WIDTH, height=HEIGHT, bg="#ffffff")
        line1 = canvas.create_text(WIDTH/2, 10, anchor=tk.CENTER, text="")
        line2 = canvas.create_text(WIDTH/2, 30, anchor=tk.CENTER, text=" ")
        canvas.pack()
        return canvas, line1, line2

    def message_frame(self, line1, line2, agent, s, r):
        if self.finished is True:
            self.canvas.itemconfig(line1, text="There is a winner!")
            self.canvas.itemconfig(line2, text="It is Agent " + str(self.winner))
            return
        suggestion = "Agent "+ str(agent + 1) +" asks Agent " + str(((agent + 1) % self.num_agents) + 1) + " for cards: " + str(s)
        answer = "Agent "+ str(((agent +1) % self.num_agents) + 1) + " responds with " + str(r)
        self.canvas.itemconfig(line1, text=suggestion)
        self.canvas.itemconfig(line2, text=answer)
        self.canvas.pack()
        return


    def update_table(self):
        if self.finished is True:
            print("the winner is already known!")
            self.message_frame(self.line1, self.line2, 0, "s", "r")
            return
        # the model takes one agent's turn
        self.last_agent += 1
        self.last_agent %= len(self.model.agents)
        agent_turn = self.model.get_agents()[self.last_agent]
        s,r = agent_turn.step()  # KB is updated during the step
        self.KB, self.unknown_cards = self.model.knowledge_dict, self.model.unknown_cards
        self.input_KB_table()  # put KB knowledge in the table
        self.message_frame(self.line1, self.line2, self.last_agent, s,r)
        if self.finished is True:
            main.loop_strategies()

    def refresh_button(self):
        refresh_button = tk.Button(self.win, text="Next Agent's turn", command=self.update_table)
        refresh_button.pack(pady=5)

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
        self.tree.pack()

        return

    def input_KB_table(self):
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
                self.winner.append(agent)
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

def init_window(num_agents, num_cards):
    """"This initializes the window"""
    win = tk.Tk()
    # title
    win.title('A model of Clue')
    # dimensions
    dim = str(num_agents * 150 + 150) + "x" + str(num_cards * 25 + 150)
    win.geometry(dim)
    # background color
    win['bg'] = '#d61e1e'

    main_frame = tk.Frame(win)
    main_frame.pack(pady=5)
    return win