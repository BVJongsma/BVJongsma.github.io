import tkinter as tk
from tkinter import ttk
import Implementation.src.cards as c


def init_table(num_agents, num_cards):
    win = tk.Tk()
    # title
    win.title('A model of Clue')
    # dimensions
    dim = str(num_agents*150+150) + "x" + str(num_cards*25+25)
    win.geometry(dim)
    # background color
    win['bg'] = '#d61e1e'
    return win


class GameInterface:
    def __init__(self, num_agents, num_cards):
        self.num_agents = num_agents
        self.num_cards = num_cards
        self.win = init_table(num_agents, num_cards)
        # start tree
        columns = ('items',)
        for i in range(1, num_agents+1):
            columns += ('agent' + str(i),)
        self.tree = ttk.Treeview(self.win, column=columns, show='headings', height=num_cards)
        self.tree.pack()
        self.init_table_information()
        self.win.mainloop()
        self.insert_player_cards()

    def update_table(self):
        # temporary update function
        self.tree.insert('', tk.END, values=(
            'extra info', '?', '?', '?'))  # if '' is replaced by selected, only adds this column once

    def refresh_button(self):
        refresh_button = tk.Button(self.win, text="Refresh Table", command=self.update_table)
        refresh_button.pack()

    def init_table_information(self):
        # define columns and headings
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.heading("#0", text="", anchor=tk.CENTER)
        self.tree.column('items', anchor=tk.CENTER, width=150)
        self.tree.heading('items', text='Items')
        # make the agent columns & headings
        for i in range(1, self.num_agents+1):
            self.tree.column('agent' + str(i), anchor=tk.CENTER, width=150)
            self.tree.heading('agent' + str(i), text='Agent ' + str(i))

        # generate list of data to put in the table
        card = c.Cards(3)
        cards = card.get_all_cards()
        question = tuple()
        for i in range(self.num_agents):
            question += ('?',)
        data = [(x,) + question for x in cards]

        # put data in the table
        for d in data:
            self.tree.insert('', tk.END,
                             values=d)  # tk.END means add at the end of the list, '0' means add at the beginning

        # add an update button
        self.refresh_button()
        self.tree.pack()

        return

    def insert_player_cards(self):
        return


if __name__ == "__main__":
    interface = GameInterface(3, 8)
