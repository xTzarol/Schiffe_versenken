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
        self.grid_height = (2 * self.grid_length) + 1
        self.create_board()

        #make the grid expandable
        for x in range(self.grid_length):
            self.f1.columnconfigure(x, weight = 1)
        for y in range(self.grid_height):
            self.f1.rowconfigure(y, weight = 1)

    #Create playing field (opponent - middle line - own field)
    def create_board(self):

        buttonsincol = []
        emptylist = []

        for x in range(self.grid_length):
            GUI.allbuttons.append(buttonsincol)
            buttonsincol = emptylist
            for y in range(self.grid_length):
                b = tk.Button(master=self.f1, bg = 'deep sky blue', fg = 'deep sky blue', state = 'disabled')
                b.grid(row=y, column=x, sticky=tk.N+tk.S+tk.E+tk.W)
                b.data=(x, y)
                b.bind("<ButtonPress-1>", self.check_for_valid_shot)
                b.grid_remove()
                buttonsincol.append(b)

        GUI.__l = tk.Label(master=self.f1, bg = 'grey')
        GUI.__l.grid(row=10, columnspan = 10, sticky=tk.N+tk.S+tk.E+tk.W)
        
        for x in range(self.grid_length):
            GUI.ownbuttons.append(buttonsincol)
            GUI.allbuttons.append(buttonsincol)
            buttonsincol = emptylist
            for y in range(self.grid_length + 1, self.grid_height):
                b = tk.Button(master=self.f1,
                              bg = 'deep sky blue', fg = 'deep sky blue')
                b.grid(row=y, column=x, sticky=tk.N+tk.S+tk.E+tk.W)
                b.data=(x, y)
                b.bind('<ButtonPress-1>', Gamelogic.place_ships)
                buttonsincol.append(b)

        GUI.show_shipsize(4)

    def show_shipsize(size):
        if size > 0:
            GUI.__l.configure(text = str(size))
        else:
            GUI.__l.configure(text = '')
    
    def tell_winner(player):
        for x in range(len(GUI.allbuttons)):
            for y in range (len(GUI.allbuttons[x])):
                GUI.allbuttons[x][y].grid_remove() 
                GUI.allbuttons[x][y].configure(state = 'disabled')
        
        if player == 1:

            GUI.__l.configure(text = 'You have won!', bg = 'lawn green')
        
        else:
            
            GUI.__l.configure(text = 'You have lost!', bg = 'red2')

    #Buttons des gegners werden Rot
    def check_for_valid_shot(self, event):
        if event.widget['state'] == 'normal':
            if Gamelogic.get_enemy_turn() == False:
                if event.widget not in GUI.__ownshots:
                    event.widget.configure(bg = 'grey')
                    event.widget.configure(text = '')
                    GUI.__ownshots.append(event.widget)
                    shot = list(event.widget.data)
                    shot.insert(0, 's')
                    Gamelogic.send_shot(tuple(shot))

    def mark_enemy_hit():
        GUI.__ownshots[len(GUI.__ownshots) - 1].configure(bg = 'red')

    def mark_own_hit(ship):
        ship.configure(bg = 'red')

class Gamelogic:

    __buttonspressed = []
    __ships = []
    __enemyshots = []
    __shipcount = 4
    enemy_ready = False
    __enemies_turn = True
    __winner = False
    
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
                            for y in range(len(GUI.ownbuttons[x])):

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
                                        #Bug, dass ermittelte Knöpfe zu oft in Gamelogic.__ships geschrieben werden (10x), Herkunft des Fehlers konnte nicht gefunden werden
                                        if GUI.ownbuttons[x][y] not in Gamelogic.__ships:
                                            Gamelogic.__ships.append(GUI.ownbuttons[x][y])

                                    if Gamelogic.__buttonspressed[len(
                                        Gamelogic.__buttonspressed) - 1].data[
                                        0] < GUI.ownbuttons[x][y].data[
                                        0] < Gamelogic.__buttonspressed[
                                        len(Gamelogic.__buttonspressed) - 2].data[0]:
                                        GUI.ownbuttons[x][y].configure(
                                        bg = 'black', fg = 'black')
                                        #Bug, dass ermittelte Knöpfe zu oft in Gamelogic.__ships geschrieben werden (10x), Herkunft des Fehlers konnte nicht gefunden werden
                                        if GUI.ownbuttons[x][y] not in Gamelogic.__ships:
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
                            for y in range(len(GUI.ownbuttons[x])):

                                #Check ob dazwischenliegender Button auf gleicher x Koordinate liegt wie äußere Buttons
                                if GUI.ownbuttons[x][y].data[0] == Gamelogic.__buttonspressed[len(Gamelogic.__buttonspressed) - 1].data[0]:

                                    #Checks ob dazwischenliegender Button zwischen äußeren Buttons liegt
                                    if Gamelogic.__buttonspressed[len(Gamelogic.__buttonspressed) - 2].data[1] < GUI.ownbuttons[x][y].data[1] < Gamelogic.__buttonspressed[len(Gamelogic.__buttonspressed) - 1].data[1]:
                                        GUI.ownbuttons[x][y].configure(bg = 'black', fg = 'black')
                                        #Bug, dass ermittelte Knöpfe zu oft in Gamelogic.__ships geschrieben werden (10x), Herkunft des Fehlers konnte nicht gefunden werden
                                        if GUI.ownbuttons[x][y] not in Gamelogic.__ships:
                                            Gamelogic.__ships.append(GUI.ownbuttons[x][y])

                                    if Gamelogic.__buttonspressed[len(Gamelogic.__buttonspressed) - 1].data[1] < GUI.ownbuttons[x][y].data[1] < Gamelogic.__buttonspressed[len(Gamelogic.__buttonspressed) - 2].data[1]:
                                        GUI.ownbuttons[x][y].configure(bg = 'black', fg = 'black')
                                        #Bug, dass ermittelte Knöpfe zu oft in Gamelogic.__ships geschrieben werden (10x), Herkunft des Fehlers konnte nicht gefunden werden
                                        if GUI.ownbuttons[x][y] not in Gamelogic.__ships:
                                            Gamelogic.__ships.append(GUI.ownbuttons[x][y])
                                        
                        Gamelogic.__shipcount -= 1
                        GUI.show_shipsize(Gamelogic.__shipcount)

        if Gamelogic.__shipcount == 0:
            Gamelogic.send_ready()
            while True:
                if Gamelogic.enemy_ready == True:
                    for x in range(len(GUI.allbuttons)):
                        for y in range (len(GUI.allbuttons[x])):
                            GUI.allbuttons[x][y].grid() 
                            GUI.allbuttons[x][y].configure(state = 'normal')
                    Gamelogic.__shipcount -= 1
                    Gamelogic.__ships = list(set(Gamelogic.__ships))
                break
  
        if Gamelogic.__shipcount < 0:
            print("Es wurden bereits alle Schiffe platziert!")
    
    def give_shipsize():
        return Gamelogic.__shipcount

    #Funktion send_data() einbringen da alle nachfolgenden Funktionen fast dasselbe tun

    def send_ready():
        Network.get_client().send(pickle.dumps("ready"))

    def send_shot(data):
        if Gamelogic.__enemies_turn == False:
            Network.get_client().send(pickle.dumps(data))
            Gamelogic.__enemies_turn = True
    
    def send_hit():
        Network.get_client().send(pickle.dumps("hit"))
        Gamelogic.set_enemy_turn_to_True()

    def send_loss():
        Network.get_client().send(pickle.dumps("won"))

    def check_for_hit(shot):
        for i in range(len(Gamelogic.__ships)):
            if (Gamelogic.__ships[i].data[0] == shot[0]) and (Gamelogic.__ships[i].data[1] == shot[1]):
                Gamelogic.send_hit()
                GUI.mark_own_hit(Gamelogic.__ships[i])

    def handle_shot(shot):
        shot = list(shot)
        shot.pop(0)
        for x in range(len(GUI.ownbuttons)):
            for y in range (len(GUI.ownbuttons[x])):
                if (GUI.ownbuttons[x][y].data[0] == shot[0]) and (GUI.ownbuttons[x][y].data[1] == shot[1]):
                    GUI.ownbuttons[x][y].configure(bg = 'grey')
                    Gamelogic.__enemyshots.append(GUI.ownbuttons[x][y])
                    Gamelogic.__enemyshots = list(set(Gamelogic.__enemyshots))
                    Gamelogic.set_enemy_turn_to_False()
                    Gamelogic.check_for_hit(shot)
                    #Bug dass Knöpfe öfter in GUI.__ownbuttons stehen
                    if set(Gamelogic.__ships).issubset(Gamelogic.__enemyshots) and Gamelogic.__winner == False:
                        Gamelogic.__winner = True
                        GUI.tell_winner(0)
                        Gamelogic.send_loss()



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
                    
            elif pickle.loads(from_server)[0] == "s":
                Gamelogic.handle_shot(pickle.loads(from_server))

            elif pickle.loads(from_server) == "ready":
                Gamelogic.enemy_ready = True

            elif pickle.loads(from_server) == "hit":
                Gamelogic.set_enemy_turn_to_False()
                GUI.mark_enemy_hit()
            
            elif pickle.loads(from_server) == "won":
                GUI.tell_winner(1)

    def get_client():
        return Network.__client

if __name__ == '__main__':

    Network.read_config()
    Network.connect_to_server()
    tk_window = tk.Tk()
    tk_window.title('Schiffe versenken')
    app = GUI(tk_window)
    app.mainloop()
    


