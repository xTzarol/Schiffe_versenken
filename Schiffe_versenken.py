#PEP8 beachten!
import tkinter as tk
from tkinter import messagebox
import configparser
import threading
import socket
import sys
import pickle

class GUI(tk.Frame):

    allbuttons = []
    ownbuttons = []
    __l = None
    __enemy_button = None
    __ownshots = []

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
            GUI.allbuttons.append(list(set(buttonsincol)))
            buttonsincol = emptylist
            for y in range(self.grid_length):
                b = tk.Button(master=self.f1, bg = 'deep sky blue', fg = 'deep sky blue', state = 'disabled')
                b.grid(row=y, column=x, sticky=tk.N+tk.S+tk.E+tk.W)
                b.data=(x, y)
                b.bind("<ButtonPress-1>", self.check_for_valid_shot)
                buttonsincol.append(b)
                b.grid_remove()

        for x in range(self.grid_length):
            for y in range(self.grid_length, self.grid_height
                           - self.grid_length):
        
                if y == 10 and x == 0:
                    GUI.__l = tk.Label(master=self.f1, bg = 'grey')
                    GUI.__l.grid(row=y, column=x, sticky=tk.N+tk.S+tk.E+tk.W)

                #Möglichkeit finden, um ein großes Label zu haben, statt mehreren kleinen damit Textkonfiguration funktioniert ohne die Größe des Grids zu verändern
                #großes Label soll auch Informationen wie Verbunden usw beinhalten

                #elif y == 10 and x == 1:
                    #l = tk.Label(master=self.f1, bg = 'grey', text = 'aktuelle Schiffslänge')
                    #l.grid(row=y, column=x, sticky=tk.N+tk.S+tk.E+tk.W)

                else:
                    l = tk.Label(master=self.f1, bg = 'grey')
                    l.grid(row=y, column=x, sticky=tk.N+tk.S+tk.E+tk.W)
    
        
        for x in range(self.grid_length):
            GUI.ownbuttons.append(list(set(buttonsincol)))
            GUI.allbuttons.append(list(set(buttonsincol)))
            buttonsincol = emptylist
            for y in range(self.grid_length + 1, self.grid_height):
                b = tk.Button(master=self.f1,
                              bg = 'deep sky blue', fg = 'deep sky blue')
                b.grid(row=y, column=x, sticky=tk.N+tk.S+tk.E+tk.W)
                buttonsincol.append(b)
                b.data=(x, y)
                b.bind('<ButtonPress-1>', Gamelogic.place_ships)

        GUI.show_shipsize(4)

    def show_shipsize(size):
        GUI.__l.configure(text=str(size))

    #Buttons des gegners werden Rot
    def check_for_valid_shot(self, event):
        if event.widget['state'] == 'normal':
            if Gamelogic.get_enemy_turn() == False:
                if event.widget not in GUI.__ownshots:
                    event.widget.configure(bg='red')
                    event.widget.configure(text='')
                    GUI.__ownshots.append(event.widget)
                    Gamelogic.send_shot(event.widget.data)
        
class Gamelogic:

    __buttonspressed = []
    __ships = []
    __enemyshots = []
    __shipcount = 4
    enemy_ready = False
    __enemies_turn = True
    
    @staticmethod
    def place_ships(event):
        #insgesamt muss  User 8 valide, äußere Buttons drücken, um alle Schiffe zu setzen

        if Gamelogic.__shipcount >= 1:

            #graues Label mit momentaner Schifflänge beschreiben
            Gamelogic.__buttonspressed.append(event.widget)

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
                        bg = 'black', fg = 'black')
                        Gamelogic.__ships.append(Gamelogic.__buttonspressed[len(
                        Gamelogic.__buttonspressed) - 2])
                        Gamelogic.__buttonspressed[
                        len(Gamelogic.__buttonspressed) - 1].configure(
                        bg = 'black', fg = 'black')
                        Gamelogic.__ships.append(Gamelogic.__buttonspressed[len(Gamelogic.__buttonspressed) - 1])

                        #Zwischen den beiden äußeren Buttons müssen alle dazwischenliegenden ebenfalls schwarz gemacht werden
                        for x in range(len(GUI.ownbuttons)):
                            for y in range (len(GUI.ownbuttons[x])):

                                #Check ob dazwischenliegender Button auf gleicher y Koordinate liegt wie äußere Buttons
                                if GUI.ownbuttons[x][y].data[1] == Gamelogic.__buttonspressed[
                                    len(Gamelogic.__buttonspressed) - 1].data[1]:

                                    #Checks ob dazwischenliegender Button zwischen äußeren Buttons liegt
                                    if Gamelogic.__buttonspressed[len(
                                        Gamelogic.__buttonspressed) - 2].data[
                                        0] < GUI.ownbuttons[x][y].data[
                                        0] < Gamelogic.__buttonspressed[
                                        len(Gamelogic.__buttonspressed) - 1].data[0]:
                                        GUI.ownbuttons[x][y].configure(
                                        bg = 'black', fg = 'black')
                                        Gamelogic.__ships.append(GUI.ownbuttons[x][y])

                                    if Gamelogic.__buttonspressed[len(
                                        Gamelogic.__buttonspressed) - 1].data[
                                        0] < GUI.ownbuttons[x][y].data[
                                        0] < Gamelogic.__buttonspressed[
                                        len(Gamelogic.__buttonspressed) - 2].data[0]:
                                        GUI.ownbuttons[x][y].configure(
                                        bg = 'black', fg = 'black')
                                        Gamelogic.__ships.append(GUI.ownbuttons[x][y])
                                        
                        #erst wenn alle Abfragen erfüllt sind wird zum nächsten Schiff übergegangen
                        Gamelogic.__shipcount -= 1
                        GUI.show_shipsize(Gamelogic.__shipcount)

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
                        bg = 'black', fg = 'black')
                        Gamelogic.__ships.append(Gamelogic.__buttonspressed[
                        len(Gamelogic.__buttonspressed) - 2])
                        Gamelogic.__buttonspressed[len(
                        Gamelogic.__buttonspressed) - 1].configure(
                        bg = 'black', fg = 'black')
                        Gamelogic.__ships.append(
                        Gamelogic.__buttonspressed[
                        len(Gamelogic.__buttonspressed) - 1])
                        
                        #Zwischen den beiden äußeren Buttons müssen alle dazwischenliegenden ebenfalls schwarz gemacht werden
                        for x in range(len(GUI.ownbuttons)):
                            for y in range (len(GUI.ownbuttons[x])):

                                #Check ob dazwischenliegender Button auf gleicher x Koordinate liegt wie äußere Buttons
                                if GUI.ownbuttons[x][y].data[0] == Gamelogic.__buttonspressed[
                                    len(Gamelogic.__buttonspressed) - 1].data[0]:

                                    #Checks ob dazwischenliegender Button zwischen äußeren Buttons liegt
                                    if Gamelogic.__buttonspressed[len(Gamelogic.__buttonspressed) - 2].data[1] < GUI.ownbuttons[x][y].data[1] < Gamelogic.__buttonspressed[len(Gamelogic.__buttonspressed) - 1].data[1]:
                                        GUI.ownbuttons[x][y].configure(bg = 'black', fg = 'black')
                                        Gamelogic.__ships.append(GUI.ownbuttons[x][y])

                                    if Gamelogic.__buttonspressed[len(Gamelogic.__buttonspressed) - 1].data[1] < GUI.ownbuttons[x][y].data[1] < Gamelogic.__buttonspressed[len(Gamelogic.__buttonspressed) - 2].data[1]:
                                        GUI.ownbuttons[x][y].configure(bg = 'black', fg = 'black')
                                        Gamelogic.__ships.append(GUI.ownbuttons[x][y])
                                        
                        Gamelogic.__shipcount -= 1
                        GUI.show_shipsize(Gamelogic.__shipcount)

        if Gamelogic.__shipcount == 0:
            Gamelogic.send_ready()
            if Gamelogic.enemy_ready == True:
                for x in range(len(GUI.allbuttons)):
                    for y in range (len(GUI.allbuttons[x])):
                        GUI.allbuttons[x][y].grid() 
                        GUI.allbuttons[x][y].configure(state = 'normal')
                Gamelogic.__shipcount -= 1
                Gamelogic.__ships = list(set(Gamelogic.__ships))
  
        if Gamelogic.__shipcount < 0:
            print("Es wurden bereits alle Schiffe platziert!")
    
    def give_shipsize():
        return Gamelogic.__shipcount

    def send_ready():
        Network.get_client().send(pickle.dumps("ready"))

    def send_shot(data):
        if Gamelogic.__enemies_turn == False:
            Network.get_client().send(pickle.dumps(data))
            Gamelogic.__enemies_turn = True
    
    def send_hit():
        Network.get_client().send(pickle.dumps("hit"))
        Gamelogic.set_enemy_turn_to_True()

    def check_for_hit(shot):
        for i in range(len(Gamelogic.__ships)):
            if (Gamelogic.__ships[i].data[0] == shot[0]) and (Gamelogic.__ships[i].data[1] == shot[1]):
                Gamelogic.send_hit()

    def handle_shot(shot):
        for x in range(len(GUI.ownbuttons)):
            for y in range (len(GUI.ownbuttons[x])):
                if (GUI.ownbuttons[x][y].data[0] == shot[0]) and (GUI.ownbuttons[x][y].data[1] == shot[1]):
                    GUI.ownbuttons[x][y].configure(bg = 'grey')
                    Gamelogic.__enemyshots.append(GUI.ownbuttons[x][y])
                    Gamelogic.__enemyshots = list(set(Gamelogic.__enemyshots))
                    Gamelogic.set_enemy_turn_to_False()
                    Gamelogic.check_for_hit(shot)
                    print(Gamelogic.__ships, Gamelogic.__enemyshots)
                    if Gamelogic.__ships == Gamelogic.__enemyshots:
                        print("Das Spiel ist vorbei, Gegner hat gewonnen!")

    def get_enemy_turn():
        return Gamelogic.__enemies_turn

    def set_enemy_turn_to_False():
        Gamelogic.__enemies_turn = False

    def set_enemy_turn_to_True():
        Gamelogic.__enemies_turn = True      

class Network:

    __client = None
    __HOST_PORT = 0
    __HOST_ADDRESS = ""

    def read_config():
        config = configparser.ConfigParser()
        config.read('serverconfig.ini')
        Network.__HOST_ADDRESS = config.get('SERVER', 'HOST_ADDRESS')
        Network.__HOST_PORT = config.get('SERVER', 'HOST_PORT') 

    def connect_to_server():
        try:
            Network.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            Network.__client.connect((Network.__HOST_ADDRESS, int(Network.__HOST_PORT)))
            t = threading.Thread(target = Network.receive_message_from_server, args = (Network.__client, ))
            t.start()
        
        except:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(title="Connection Error", message="Cannot connect to server: " + Network.__HOST_ADDRESS + " on port: " + str(Network.__HOST_PORT))
            sys.exit()

    def receive_message_from_server(server_connection):

        while True:
            from_server = server_connection.recv(4096)

            if not from_server:
                break   

            if from_server.startswith("welcome".encode()):
                if from_server == "welcome1".encode():
                    #mit Labels machen sodass cmd überflüssig
                    print("Welcome Player 1. Waiting for Player 2!")
                    Gamelogic.set_enemy_turn_to_False()
                elif from_server == "welcome2".encode():
                    print("Welcome Player 2. The game will start soon!")
                    
            elif isinstance(pickle.loads(from_server), tuple) == True:
                Gamelogic.handle_shot(pickle.loads(from_server))

            elif pickle.loads(from_server) == "ready":
                Gamelogic.enemy_ready = True

            elif pickle.loads(from_server) == "hit":
                print("received hit")
                Gamelogic.set_enemy_turn_to_False()

    def get_client():
        return Network.__client

if __name__ == '__main__':

    Network.read_config()
    Network.connect_to_server()
    tk_window = tk.Tk()
    tk_window.title('Schiffe versenken')
    app = GUI(tk_window)
    app.mainloop()
    


