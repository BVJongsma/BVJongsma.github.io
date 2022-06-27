import tkinter as tk
from tkinter import ttk


def init_table():
    win = tk.Tk()
    # title
    win.title('A model of Clue')
    # dimensions
    win.geometry("650x250")
    # background color
    win['bg'] = '#d61e1e'
    # s = ttk.Style()
    # s.theme_use('clam')

    return win


class GameInterface:
    def __init__(self):
        self.win = init_table()
        # start tree
        columns = ('items', 'agent1', 'agent2', 'agent3')
        self.tree = ttk.Treeview(self.win, column=columns, show='headings')
        self.tree.pack()
        self.init_table_information()
        self.win.mainloop()
        self.insert_player_cards()

    def update_table(self):
        selected = self.tree.focus()
        self.tree.insert(selected, tk.END, values=(
            'extra info', '?', '?', '?'))  # if '' is replaced by selected, only adds this column once

    def insert_button(self):
        refresh_button = tk.Button(self.win, text="Refresh Table", command=self.update_table)
        refresh_button.pack()

    def init_table_information(self):
        # define columns and headings
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.heading("#0", text="", anchor=tk.CENTER)
        self.tree.column('items', anchor=tk.CENTER, width=150)
        self.tree.heading('items', text='Items')
        self.tree.column('agent1', anchor=tk.CENTER, width=150)
        self.tree.heading('agent1', text='Agent 1')
        self.tree.column('agent2', anchor=tk.CENTER, width=150)
        self.tree.heading('agent2', text='Agent 2')
        self.tree.column('agent3', anchor=tk.CENTER, width=150)
        self.tree.heading('agent3', text='Agent 3')

        # generate list of data to put in the table
        suspects = ['Scarlet', 'Mustard', 'Green', 'Plum']
        weapons = ['candlestick', 'dagger', 'rope', 'wrench']
        cards = suspects + weapons
        data = [(x, '?', '?', '?') for x in cards]

        # put data in the table
        for d in data:
            self.tree.insert('', tk.END,
                             values=d)  # tk.END means add at the end of the list, '0' means add at the beginning

        self.insert_button()

        self.tree.pack()

        return

    def insert_player_cards(self):
        return


if __name__ == "__main__":
    interface = GameInterface()

# Insert the data in Treeview widget
# tree.insert('', 'end', text="1", values=('1', 'Joe', 'Nash'))
# tree.insert('', 'end', text="2", values=('2', 'Emily', 'Mackmohan'))
# tree.insert('', 'end', text="3", values=('3', 'Estilla', 'Roffe'))
# tree.insert('', 'end', text="4", values=('4', 'Percy', 'Andrews'))
# tree.insert('', 'end', text="5", values=('5', 'Stephan', 'Heyward'))
