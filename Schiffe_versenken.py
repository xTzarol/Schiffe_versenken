#erste (zweite) Version des Programms, PEP8 beachten!
from os import replace
import tkinter as tk
from tkinter import messagebox
import configparser
import threading
import socket
import sys
import pickle

class GUI(tk.Frame):

    allbuttons = []
    __l = None
    __enemy_button = None

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

        GUI.show_shipsize(4)

    def show_shipsize(size):
        GUI.__l.configure(text=str(size))

    #Client server Kommunikation:
    #Buttons des gegners werden Rot
    def check_for_hit(self, event):
        GUI.__enemy_button = event.widget             
        event.widget.configure(bg='red')
        event.widget.configure(text='')
        Gamelogic.send_shot()
    
    def get_enemy_button():
        return GUI.__enemy_button.data
        

#Bugfix dass wenn alle Schiffe platziert wurden tatsächlich richtiger Print erfolgt
class Gamelogic:

    __buttonspressed = []
    __ships = []
    __shipcount = 4
    __shots = []
    
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
                    GUI.show_shipsize(Gamelogic.__shipcount - 1)

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

                                    if Gamelogic.__buttonspressed[len(Gamelogic.__buttonspressed) - 1].data[1] < GUI.allbuttons[x][y].data[1] < Gamelogic.__buttonspressed[len(Gamelogic.__buttonspressed) - 2].data[1]:
                                        GUI.allbuttons[x][y].configure(bg='black')
                                        Gamelogic.__ships.append(GUI.allbuttons[x][y])
                                        
                        Gamelogic.__shipcount -= 1

        else:
            print("Es wurden bereits alle Schiffe platziert!")
    
    def give_shipsize():
        return Gamelogic.__shipcount

    def send_ready():
        Network.get_client().send(pickle.dumps("ready"))

    def send_shot():
        Network.get_client().send(pickle.dumps(GUI.get_enemy_button()))

    def handle_shot(shot):
        for x in range(len(GUI.allbuttons)):
            for y in range (len(GUI.allbuttons[x])):
                if (GUI.allbuttons[x][y].data[0] == shot[0]) and (GUI.allbuttons[x][y].data[1] == shot[1]):
                    GUI.allbuttons[x][y].configure(bg='grey')
                    Gamelogic.__shots.append(GUI.allbuttons[x][y])      

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
                elif from_server == "welcome2".encode():
                    print("Welcome Player 2. The game will start soon!")
                    
                elif isinstance(pickle.loads(from_server), tuple) == True: 
                    Gamelogic.handle_shot(pickle.loads(from_server))

            if from_server == "start_game":
                return 

    def get_client():
        return Network.__client

if __name__ == '__main__':

    Network.read_config()
    Network.connect_to_server()
    tk_window = tk.Tk()
    tk_window.title('Schiffe versenken')
    app = GUI(tk_window)
    app.mainloop()
    


