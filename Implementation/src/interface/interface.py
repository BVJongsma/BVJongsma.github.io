import tkinter as tk
from tkinter import ttk
import Implementation.src.cards as ca
import main

class GameInterface:
    """"
    The interface of the game: this shows a table displaying what information each agent has.
    The columns show a database of what each agent knows.
    The rows show the different cards.
    e.g. If in column "Agent 1", row "dagger" it says: "Agent 3", this means that Agent 1 knows that Agent 3 has the card "dagger".
    A '?' means that the agent still does not know where the card is.
    """
    def __init__(self, model):
        """"
        Initialising the Gameinterface.
        """
        #Initialise model and values
        self.model = model
        self.num_agents = model.num_agents
        cards_set = ca.Cards(self.num_agents, self.model.num_weapons, self.model.num_suspects)
        self.num_cards = len(cards_set.get_all_cards())
        self.win = init_window(self.num_agents, self.num_cards)
        self.last_agent = -1
        self.finished = False
        self.winner = []
        # initialise table structure
        columns = ('items',)
        for i in range(1, self.num_agents + 1):
            columns += ('agent' + str(i),)
        self.tree = ttk.Treeview(self.win, column=columns, show='headings', height=(self.num_cards + 1))
        self.KB, self.unknown_cards = self.model.kripke_model.initialise_known_dictionary(self.model.agents)
        self.tree.pack()
        #input table information
        self.init_table_information()
        self.input_KB_table()
        #input 'Next Agent's turn' button
        self.refresh_button()
        #input message box
        self.canvas, self.line1, self.line2 = self.message_frame_init()
        #Let the interface run
        self.win.mainloop()

    def message_frame_init(self):
        """"
        initialise the message frame
        :returns
            canvas: type tk.Canvas, the canvas in which text is written.
            line1: type tk.Canvas.create_text, line 1 of the text.
            line2: type tk.Canvas.create_text, line 2 of the text.
        """
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
        """"
        The message box of the interface is updated.
        :returns
            line1: type tk.Canvas.create_text
            line2: type tk.Canvas.create_text
            agent: type int. The agent which turn it is. This is the agent that asks the question.
            s: type List[String]. the cards the agent asks for.
            r: type String. the response from the other agent: either a weapon card, color card or None.
        """
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
        """"
        When refresh_button is pressed, the next agent takes it turn.
        The relations and KB are updated, after which
        the table as shown in the interface and the message box are updated.
        """
        if self.finished is True:
            print("the winner is already known!")
            return
        # the model takes one agent's turn
        self.last_agent += 1
        self.last_agent %= len(self.model.agents)
        agent_turn = self.model.get_agents()[self.last_agent]
        s,r = agent_turn.step()  # KB is updated during the step
        self.KB, self.unknown_cards = self.model.knowledge_dict, self.model.unknown_cards
        self.input_KB_table()  # put KB knowledge in the table
        if self.finished is True:
            self.message_frame(self.line1, self.line2, 0, "s", "r")
            return
        self.message_frame(self.line1, self.line2, self.last_agent, s, r)
        return

    def refresh_button(self):
        """"the refresh button that is seen on the interface."""
        refresh_button = tk.Button(self.win, text="Next Agent's turn", command=self.update_table)
        refresh_button.pack(pady=5)
        return

    def init_table_information(self):
        """"
        initialise the data to put in the table, before the game starts.
        This means: the names of the cards and the agent's own cards.
        """
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
        """"
        A function that updates the table. It takes the information from self.KB
        and makes new tuples, that then get added to the correct table row.
        """
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
        """"
        :returns
            values = tuple of strings, containing the relations of all the agents.
        """
        rel = self.model.kripke_model.relations
        values = ('relations',)
        for a in self.model.agents:
            values += (str(len(rel[str(a.get_unique_id())])),)
        return values

def init_window(num_agents, num_cards):
    """"
    This initializes the window
    :argument
        num_agents: the amount of agents. type: int
        num_cards: the amount of cards. type: int
    :returns
        win: the window. type: Tk
    """
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