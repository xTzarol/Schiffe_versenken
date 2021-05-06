#erste (zweite) Version des Programms
from tkinter import *

class GUI(Frame):
    def __init__(self, master):
        super().__init__(master) 
        master.geometry("500x550")
        #frame
        self.f1 = Frame(master=master)
        self.f1.pack(fill=BOTH, expand=True)
        #game board size
        self.grid_length = 10
        self.create_board()

        #make the grid expandable
        for x in range(self.grid_length):
            self.f1.columnconfigure(x, weight=1)
            self.f1.rowconfigure(x, weight=1)

    def create_board(self):
        for x in range(self.grid_length):
            for y in range(self.grid_length):
                b = Button(master=self.f1, text="{}/{}".format(x,y), command = self.check_for_hit, bg="white")
                b.grid(row=y, column=x, sticky=N+S+E+W)

        for x in range(self.grid_length):
            for y in range(self.grid_length, self.grid_length + 1):
                l = Label(master=self.f1, bg = "grey")
                l.grid(row=y, column=x, sticky=N+S+E+W)

        for x in range(self.grid_length):
            for y in range(self.grid_length + 1, self.grid_length + self.grid_length + 1):
                b = Button(master=self.f1, text="{}/{}".format(x,y - self.grid_length - 1), command = self.place_ships, bg="white")
                b.grid(row=y, column=x, sticky=N+S+E+W)

    def check_for_hit(self):
        self.configure(bg="black")
        print("Test")

            
    def place_ships(self):
        self.configure(bg="black")
        print("Test1")

        
if __name__ == '__main__':

    tk_window = Tk()
    tk_window.title("Schiffe versenken")
    app = GUI(tk_window)
    app.mainloop()

#Command für Rückgabe wenn auf Button gedrückt wird
    