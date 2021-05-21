#erste (zweite) Version des Programms, PEP8 beachten!
import tkinter as tk
import socket as sk

class GUI(tk.Frame):

    allbuttons = []
    __l = None

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

    #Create playing field (opponent - middle line - own field)
    def create_board(self):

        buttonsincol = []
        emptylist = []

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
        
                if y == 10 and x == 0:
                    GUI.__l = tk.Label(master=self.f1, bg = 'grey')
                    GUI.__l.grid(row=y, column=x, sticky=tk.N+tk.S+tk.E+tk.W)
                else:
                    GUI.__l = tk.Label(master=self.f1, bg = 'grey')
                    GUI.__l.grid(row=y, column=x, sticky=tk.N+tk.S+tk.E+tk.W)
    
        
        for x in range(self.grid_length):
            GUI.allbuttons.append(buttonsincol)
            buttonsincol = emptylist
            for y in range(self.grid_length + 1, self.grid_height):
                b = tk.Button(master=self.f1,
                              text='{}/{}'.format(x,y - self.grid_length - 1),
                              bg='white')
                b.grid(row=y, column=x, sticky=tk.N+tk.S+tk.E+tk.W)
                buttonsincol.append(b)
                b.data=(x, y)
                b.bind('<ButtonPress-1>', Gamelogic.place_ships)

    def give_label():
        return GUI.__l

    #Client server Kommunikation:
    #Buttons des gegners werden Rot
    def check_for_hit(self, event):             
        event.widget.configure(bg='red')
        event.widget.configure(text='')
        print("Test")

    #Funktion soll checken ob erste beiden gedrückten Buttons für
    #großes Schiff passen

class Gamelogic:

    __buttonspressed = []
    __ships = []
    __shipbuttoncount = 8
    __shipcount = 4
    
    @staticmethod
    def place_ships(event):
        #insgesamt muss  User 8 valide, äußere Buttons drücken, um alle Schiffe zu setzen
        if Gamelogic.__shipbuttoncount >= 1:
            Gamelogic.__buttonspressed.append(event.widget)

            #Zugreifen auf Variable in anderer Klasse:
            GUI.give_label().configure(text=str(Gamelogic.__shipcount))

            #Check ob 2 neue Buttons dazugekommen sind
            if len(Gamelogic.__buttonspressed) % 2 == 0:
                #horizontal, Check ob Abstand zwischen den Buttons mit momentaner Schiffslänge übereinstimmt
                if abs(Gamelogic.__buttonspressed[len(
                    Gamelogic.__buttonspressed) - 2].data[0]
                    - Gamelogic.__buttonspressed[len(
                    Gamelogic.__buttonspressed) - 1] 
                            .data[0]) + 1 == Gamelogic.__shipcount:

                    #y Koordinate muss die gleiche sein, sonst diagonal
                    if Gamelogic.__buttonspressed[len(
                        Gamelogic.__buttonspressed) - 2].data[1] == Gamelogic.__buttonspressed[
                        len(Gamelogic.__buttonspressed) - 1].data[1]:
                        print('Abstand passt', Gamelogic.__shipcount)
                        print(Gamelogic.__buttonspressed)
                        Gamelogic.__buttonspressed[len(
                        Gamelogic.__buttonspressed) - 2].configure(
                        bg='black')
                        Gamelogic.__ships.append(Gamelogic.__buttonspressed[len(
                        Gamelogic.__buttonspressed) - 2])
                        Gamelogic.__buttonspressed[
                        len(Gamelogic.__buttonspressed) - 1].configure(
                        bg='black')
                        Gamelogic.__ships.append(Gamelogic.__buttonspressed[
                        len(Gamelogic.__buttonspressed) - 1])

                        #Zwischen den beiden äußeren Buttons müssen alle dazwischenliegenden ebenfalls schwarz gemacht werden
                        for x in range(len(GUI.allbuttons)):
                            for y in range (len(GUI.allbuttons[x])):

                                #Check ob dazwischenliegender Button auf gleicher y Koordinate liegt wie äußere Buttons
                                if GUI.allbuttons[x][y].data[1] == Gamelogic.__buttonspressed[
                                    len(Gamelogic.__buttonspressed) - 1].data[1]:

                                    #Checks ob dazwischenliegender Button zwischen äußeren Buttons liegt
                                    if Gamelogic.__buttonspressed[len(
                                        Gamelogic.__buttonspressed) - 2].data[
                                        0] < GUI.allbuttons[x][y].data[
                                        0] < Gamelogic.__buttonspressed[
                                        len(Gamelogic.__buttonspressed) - 1].data[0]:
                                        GUI.allbuttons[x][y].configure(
                                        bg='black')
                                        Gamelogic.__ships.append(GUI.allbuttons[x][y])

                                    if Gamelogic.__buttonspressed[len(
                                        Gamelogic.__buttonspressed) - 1].data[
                                        0] < GUI.allbuttons[x][y].data[
                                        0] < Gamelogic.__buttonspressed[
                                        len(Gamelogic.__buttonspressed) - 2].data[0]:
                                        GUI.allbuttons[x][y].configure(
                                        bg='black')
                                        Gamelogic.__ships.append(GUI.allbuttons[x][y])
                                        
                        #erst wenn alle Abfragen erfüllt sind wird zum nächsten Schiff übergegangen
                        Gamelogic.__shipcount -= 1
                        Gamelogic.__shipbuttoncount -= 1

                #vertical, Check ob Abstand zwischen den Buttons mit momentaner Schiffslänge übereinstimmt
                if abs(Gamelogic.__buttonspressed[len(
                        Gamelogic.__buttonspressed) - 2].data[1] - 
                        Gamelogic.__buttonspressed[len(
                        Gamelogic.__buttonspressed) - 1].data[
                        1]) + 1 == Gamelogic.__shipcount:

                    #x Koordinate muss die gleiche sein, sonst diagonal
                    if Gamelogic.__buttonspressed[len(
                        Gamelogic.__buttonspressed) - 2].data[
                        0] == Gamelogic.__buttonspressed[
                        len(Gamelogic.__buttonspressed) - 1].data[0]:
                        print("Abstand passt", Gamelogic.__shipcount)
                        print(Gamelogic.__buttonspressed)
                        Gamelogic.__buttonspressed[len(
                        Gamelogic.__buttonspressed) - 2].configure(
                        bg='black')
                        Gamelogic.__ships.append(Gamelogic.__buttonspressed[
                        len(Gamelogic.__buttonspressed) - 2])
                        Gamelogic.__buttonspressed[len(
                        Gamelogic.__buttonspressed) - 1].configure(
                        bg='black')
                        Gamelogic.__ships.append(
                        Gamelogic.__buttonspressed[
                        len(Gamelogic.__buttonspressed) - 1])
                        
                        #Zwischen den beiden äußeren Buttons müssen alle dazwischenliegenden ebenfalls schwarz gemacht werden
                        for x in range(len(GUI.allbuttons)):
                            for y in range (len(GUI.allbuttons[x])):

                                #Check ob dazwischenliegender Button auf gleicher x Koordinate liegt wie äußere Buttons
                                if GUI.allbuttons[x][y].data[0] == Gamelogic.__buttonspressed[
                                    len(Gamelogic.__buttonspressed) - 1].data[0]:

                                    #Checks ob dazwischenliegender Button zwischen äußeren Buttons liegt
                                    if Gamelogic.__buttonspressed[
                                        len(Gamelogic.__buttonspressed) - 2].data[
                                        1] < GUI.allbuttons[x][y].data[
                                        1] < Gamelogic.__buttonspressed[
                                        len(Gamelogic.__buttonspressed) - 1].data[1]:
                                        GUI.allbuttons[x][y].configure(
                                        bg='black')
                                        Gamelogic.__ships.append(GUI.allbuttons[x][y])

                                    if Gamelogic.__buttonspressed[
                                        len(Gamelogic.__buttonspressed) - 1].data[
                                        1] < GUI.allbuttons[x][y].data[
                                        1] < Gamelogic.__buttonspressed[
                                        len(Gamelogic.__buttonspressed) - 2].data[1]:
                                        GUI.allbuttons[x][y].configure(
                                        bg='black')
                                        Gamelogic.__ships.append(GUI.allbuttons[x][y])

                        Gamelogic.__shipcount -= 1
                        Gamelogic.__shipbuttoncount -= 1


                #daten von Knopf der gedrückt wird in Liste schreiben
                #Idee (x, y) (x, y)...
                #wenn Länge von Liste%2 --> checken ob Koordinaten der letzten beiden
                #Knöpfe für Schiffsgröße (__shipcount) richtig liegen (x-__shipcount)
                #oder (y-__shipcount), sonst letzten Eintrag aus Liste löschen und
                #print("ungültiges Feld!")
                #Idee um dazwischenliegende Felder schwarz anzumalen
                #Durch alle Buttons durchiterieren und mit if Abfragen ob Koordinate unter .data mit jener 
                #von Buttons -1, -2, -3 usw. übereinstimmt   
      
            else:
                print("Es wurden bereits alle Schiffe platziert!")
        
#shipcords[1][1].configure(bg="blue")
#event.widget.configure(bg='black')
#event.widget.configure(text='')

#unklar ob neue Klasse für Spielablauf empfohlen ist?
#class Gamelogic:
    #def check_for_hit(self)

        
if __name__ == '__main__':

    tk_window = tk.Tk()
    tk_window.title('Schiffe versenken')
    app = GUI(tk_window)
    app.mainloop()
    Logic = Gamelogic
    

        

