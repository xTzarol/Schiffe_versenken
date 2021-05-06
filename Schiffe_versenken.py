<<<<<<< HEAD
#erste (zweite) Version des Programms
from tkinter import *

class GUI(Frame):
=======
#erste (zweite) Version des Programms, PEP8 beachten!
import tkinter as tk
class GUI(tk.Frame):
>>>>>>> 2550cd38489da6ead9fb21c68da0ab7282e75644
    def __init__(self, master):
        super().__init__(master) 
        master.geometry('500x550')
        #frame
        self.f1 = tk.Frame(master=master)
        self.f1.pack(fill=tk.BOTH, expand=True)
        #game board size
        self.grid_length = 10
        self.grid_height = 2 * self.grid_length + 1
        self.create_board()

        #make the grid expandable
        for x in range(self.grid_length):
            self.f1.columnconfigure(x, weight=1)
        for y in range(self.grid_height):
            self.f1.rowconfigure(y, weight=1)

    def create_board(self):
        for x in range(self.grid_length):
            for y in range(self.grid_length):
                b = tk.Button(master=self.f1, text='{}/{}'.format(x,y),
                              bg='white')
                b.grid(row=y, column=x, sticky=tk.N+tk.S+tk.E+tk.W)
                b.data=(x, y)
                b.bind("<ButtonPress-1>", self.check_for_hit)

        for x in range(self.grid_length):
            for y in range(self.grid_length, self.grid_height
                           - self.grid_length):
                l = tk.Label(master=self.f1, bg = 'grey')
                l.grid(row=y, column=x, sticky=tk.N+tk.S+tk.E+tk.W)

        for x in range(self.grid_length):
            for y in range(self.grid_length + 1, self.grid_height):
                b = tk.Button(master=self.f1,
                              text='{}/{}'.format(x,y - self.grid_length - 1),
                              bg='white')
                b.grid(row=y, column=x, sticky=tk.N+tk.S+tk.E+tk.W)
                b.data=(x, y)
                b.bind('<ButtonPress-1>', self.place_ships)

    #to be further extended
    def check_for_hit(self, event):             
        event.widget.configure(bg='red')
        event.widget.configure(text='')
        print("Test")

<<<<<<< HEAD
            
    def place_ships(self):
        self.configure(bg="black")
        print("Test1")
=======
    #Funktion soll checken ob erste beiden gedrückten Buttons für
    #großes Schiff passen
    #Idee: Koordinaten von ersten Knopf bzw. Data holen unnd als Variable
    #speichern,
    #evtl. gleiches für zweiten Knopf. Dann checken ob Koordinaten
    #beider Knöpfe für großes Schiff stimmen --> Ausgabe wenn Fehler
    def place_ships(self, event):
        for i in range(5):
            if f


        event.widget.configure(bg='black')
        event.widget.configure(text='')

#unklar ob neue Klasse für Spielablauf empfohlen ist?
#class Gamelogic:
    #def check_for_hit(self)
>>>>>>> 2550cd38489da6ead9fb21c68da0ab7282e75644

        
if __name__ == '__main__':

    tk_window = tk.Tk()
    tk_window.title('Schiffe versenken')
    app = GUI(tk_window)
    app.mainloop()

#Command für Rückgabe wenn auf Button gedrückt wird
    