import tkinter as tk
from tkinter import messagebox
import configparser
import threading
import socket
import os
import pickle
import time
import ctypes

class GUI(tk.Frame):

    __allbuttons = []
    __ownbuttons = []
    __ownshots = []
    __l = None

    def __init__(self, master):
        ctypes.windll.user32.ShowWindow \
        (ctypes.windll.kernel32.GetConsoleWindow(), 0)
        super().__init__(master)
        master.geometry('500x550')
        self.f1 = tk.Frame(master = master)
        self.f1.pack(fill = tk.BOTH, expand = True)
        self.grid_length = 10
        self.grid_height = (2*self.grid_length) + 1
        self.create_board()

        # make the grid expandable
        for x in range(self.grid_length):
            self.f1.columnconfigure(x, weight = 1)
        for y in range(self.grid_height):
            self.f1.rowconfigure(y, weight = 1)

    # Create playing field (opponent - middle line - own field)
    def create_board(self):

        buttonsincol = []
        emptylist = []

        for x in range(self.grid_length):
            GUI.__allbuttons.append(buttonsincol)
            buttonsincol = emptylist
            for y in range(self.grid_length):
                b = tk.Button(master=self.f1, bg = 'deep sky blue', \
                    fg = 'deep sky blue', state = 'disabled')
                b.grid(row = y, column = x, sticky = tk.N + tk.S + tk.E + tk.W)
                b.data = (x, y)
                b.bind('<ButtonPress-1>', self.check_for_valid_shot)
                b.grid_remove()
                buttonsincol.append(b)

        GUI.__l = tk.Label(master = self.f1, bg = 'grey')
        GUI.__l.grid(row = 10, columnspan = 10,
            sticky = tk.N + tk.S + tk.E + tk.W)

        for x in range(self.grid_length):
            GUI.__ownbuttons.append(buttonsincol)
            GUI.__allbuttons.append(buttonsincol)
            buttonsincol = emptylist
            for y in range(self.grid_length + 1, self.grid_height):
                b = tk.Button(master = self.f1,
                              bg = 'deep sky blue', fg = 'deep sky blue')
                b.grid(row = y, column = x, sticky = tk.N + tk.S + tk.E + tk.W)
                b.data = (x, y)
                b.bind('<ButtonPress-1>', Gamelogic.place_ships)
                buttonsincol.append(b)

        GUI.show_shipsize(4)

    def show_shipsize(size):
        if (size > 0):
            GUI.__l.configure(text = str(size))
        else:
            GUI.__l.configure(text = '')

    def tell_winner(player):
        for x in range(len(GUI.__allbuttons)):
            for y in range(len(GUI.__allbuttons[x])):
                GUI.__allbuttons[x][y].grid_remove()
                GUI.__allbuttons[x][y].configure(state = 'disabled')

        if (player == 1):
            GUI.__l.configure(text='You have won!', bg = 'lawn green')

        else:
            GUI.__l.configure(text='You have lost!', bg = 'red2')

    # Buttons des gegners werden Rot
    def check_for_valid_shot(self, event):
        if (event.widget['state'] == 'normal'):
            if (Gamelogic.get_enemy_turn() == False):
                if (event.widget not in GUI.__ownshots):
                    event.widget.configure(bg = 'grey')
                    event.widget.configure(text = '')
                    GUI.__ownshots.append(event.widget)
                    shot = list(event.widget.data)
                    shot.insert(0, 's')
                    Network.send_shot(tuple(shot))

    def welcome_player(player):
        time.sleep(0.5)
        if (player == 1):
            GUI.__l.configure(
                text = 'Willkommen Spieler 1. Warte auf Spieler 2! - 4'
                )
        else:
            GUI.__l.configure(
                text = 'Willkomen Spieler 2. Das Spiel kann beginnen! - 4'
                )

    def mark_enemy_hit():
        GUI.__ownshots[len(GUI.__ownshots) - 1].configure(bg = 'red')

    def mark_own_hit(ship):
        ship.configure(bg = 'red')

    def all_ships_placed():
        GUI.__l.configure(text = 'Es wurden bereits alle Schiffe platziert!')

    def get_all_buttons():
        return GUI.__allbuttons

    def get_own_buttons():
        return GUI.__ownbuttons

class Gamelogic:

    __buttonspressed = []
    __ships = []
    __enemyshots = []
    __shipcount = 4
    __enemy_ready = False
    __enemies_turn = True
    __winner = False

    @staticmethod
    def place_ships(event):
        # insgesamt muss  User 8 valide, äußere Buttons drücken,
        #  um alle Schiffe zu setzen

        if (Gamelogic.__shipcount >= 1):

            # graues Label mit momentaner Schifflänge beschreiben
            Gamelogic.__buttonspressed.append(event.widget)

            # Check ob 2 neue Buttons dazugekommen sind
            if (len(Gamelogic.__buttonspressed) % 2 == 0 \
            and Gamelogic.__buttonspressed \
            [len(Gamelogic.__buttonspressed) - 2] not in Gamelogic.__ships \
            and Gamelogic.__buttonspressed \
            [len(Gamelogic.__buttonspressed) - 1] not in Gamelogic.__ships):

                # horizontal, Check ob Abstand zwischen den Buttons
                #  mit momentaner Schiffslänge übereinstimmt
                if (abs(Gamelogic.__buttonspressed \
                    [len(Gamelogic.__buttonspressed) - 2].data[0] \
                    - Gamelogic.__buttonspressed \
                    [len(Gamelogic.__buttonspressed) - 1].data[0]) \
                    + 1 == Gamelogic.__shipcount):

                    # y Koordinate muss die gleiche sein, sonst diagonal
                    if (Gamelogic.__buttonspressed \
                        [len(Gamelogic.__buttonspressed) - 2].data[1] \
                        == Gamelogic.__buttonspressed \
                        [len(Gamelogic.__buttonspressed) - 1].data[1]):
                        Gamelogic.__buttonspressed \
                            [len(Gamelogic.__buttonspressed) - 2].configure(
                                bg='black', fg='black'
                                )
                        Gamelogic.__ships.append(Gamelogic.__buttonspressed \
                            [len(Gamelogic.__buttonspressed) - 2])
                        Gamelogic.__buttonspressed \
                            [len(Gamelogic.__buttonspressed) - 1].configure(
                                bg='black', fg='black'
                                )
                        Gamelogic.__ships.append(Gamelogic.__buttonspressed \
                            [len(Gamelogic.__buttonspressed) - 1])

                        # Zwischen den beiden äußeren Knöpfe müssen alle
                        # dazwischenliegenden ebenfalls schwarz gemacht werden
                        for x in range(len(GUI.get_own_buttons())):
                            for y in range(len(GUI.get_own_buttons()[x])):

                                # Check ob dazwischenliegender Knopf auf
                                # gleicher y Koordinate liegt wie äußere Knöpfe
                                if (GUI.get_own_buttons()[x][y].data[1] \
                                    == Gamelogic.__buttonspressed \
                                    [len(Gamelogic.__buttonspressed) - 1] \
                                    .data[1]):

                                    # Checks ob dazwischenliegender Button
                                    # zwischen äußeren Buttons liegt
                                    if (Gamelogic.__buttonspressed \
                                        [len(Gamelogic.__buttonspressed) \
                                        - 2].data[0] \
                                        < GUI.get_own_buttons()[x][y].data[0] \
                                        < Gamelogic.__buttonspressed \
                                        [len(Gamelogic.__buttonspressed) \
                                        - 1].data[0]):
                                        GUI.get_own_buttons()[x][y].configure(
                                            bg='black', fg='black'
                                            )
                                        if (GUI.get_own_buttons()[x][y]
                                            not in Gamelogic.__ships):
                                            Gamelogic.__ships.append(
                                                GUI.get_own_buttons()[x][y]
                                                )

                                    if Gamelogic.__buttonspressed \
                                        [len(Gamelogic.__buttonspressed) \
                                        - 1].data[0] \
                                        < GUI.get_own_buttons()[x][y].data[0] \
                                        < Gamelogic.__buttonspressed[
                                        len(Gamelogic.__buttonspressed) \
                                        - 2].data[0]:
                                        GUI.get_own_buttons()[x][y].configure(
                                            bg='black', fg='black')
                                        if GUI.get_own_buttons()[x][y] \
                                            not in Gamelogic.__ships:
                                            Gamelogic.__ships.append(
                                                GUI.get_own_buttons()[x][y]
                                                )

                        # erst wenn alle Abfragen erfüllt sind wird
                        # zum nächsten Schiff übergegangen
                        Gamelogic.__shipcount -= 1
                        GUI.show_shipsize(Gamelogic.__shipcount)

                # vertical, Check ob Abstand zwischen den Buttons mit
                # momentaner Schiffslänge übereinstimmt
                if abs(Gamelogic.__buttonspressed \
                    [len(Gamelogic.__buttonspressed) - 2].data[1] \
                    - Gamelogic.__buttonspressed \
                    [len(Gamelogic.__buttonspressed) - 1].data[1]) \
                    + 1 == Gamelogic.__shipcount:

                    # x Koordinate muss die gleiche sein, sonst diagonal
                    if Gamelogic.__buttonspressed \
                        [len(Gamelogic.__buttonspressed) - 2].data[0] \
                        == Gamelogic.__buttonspressed \
                        [len(Gamelogic.__buttonspressed) - 1].data[0]:
                        Gamelogic.__buttonspressed \
                            [len(Gamelogic.__buttonspressed) - 2].configure(
                            bg='black', fg='black'
                            )
                        Gamelogic.__ships.append(Gamelogic.__buttonspressed \
                            [len(Gamelogic.__buttonspressed) - 2])
                        Gamelogic.__buttonspressed \
                            [len(Gamelogic.__buttonspressed) - 1].configure(
                            bg='black', fg='black'
                            )
                        Gamelogic.__ships.append(Gamelogic.__buttonspressed \
                            [len(Gamelogic.__buttonspressed) - 1])

                        # Zwischen den beiden äußeren Buttons müssen alle
                        # dazwischenliegenden ebenfalls schwarz gemacht werden
                        for x in range(len(GUI.get_own_buttons())):
                            for y in range(len(GUI.get_own_buttons()[x])):

                                # Check ob dazwischenliegender Button auf
                                #  gleicher x Koordinate liegt wie äußere Buttons
                                if GUI.get_own_buttons()[x][y].data[0] \
                                    == Gamelogic.__buttonspressed \
                                    [len(Gamelogic.__buttonspressed) \
                                    - 1].data[0]:

                                    # Checks ob dazwischenliegender Button
                                    # zwischen äußeren Buttons liegt
                                    if Gamelogic.__buttonspressed \
                                        [len(Gamelogic.__buttonspressed)
                                        - 2].data[1] \
                                        < GUI.get_own_buttons()[x][y].data[1] \
                                        < Gamelogic.__buttonspressed \
                                        [len(Gamelogic.__buttonspressed) \
                                        - 1].data[1]:
                                        GUI.get_own_buttons()[x][y].configure(
                                            bg='black', fg='black'
                                            )

                                        if GUI.get_own_buttons()[x][y] \
                                            not in Gamelogic.__ships:
                                            Gamelogic.__ships.append(
                                                GUI.get_own_buttons()[x][y]
                                                )

                                    if Gamelogic.__buttonspressed \
                                        [len(Gamelogic.__buttonspressed) \
                                        - 1].data[1] \
                                        < GUI.get_own_buttons()[x][y].data[1] \
                                        < Gamelogic.__buttonspressed \
                                        [len(Gamelogic.__buttonspressed) \
                                        - 2].data[1]:
                                        GUI.get_own_buttons()[x][y].configure(
                                            bg='black', fg='black'
                                            )

                                        if GUI.get_own_buttons()[x][y] \
                                            not in Gamelogic.__ships:
                                            Gamelogic.__ships.append(
                                                GUI.get_own_buttons()[x][y]
                                                )

                        Gamelogic.__shipcount -= 1
                        GUI.show_shipsize(Gamelogic.__shipcount)

        if Gamelogic.__shipcount == 0:
            Network.send_data('ready')
            if Gamelogic.__enemy_ready == True:
                for x in range(len(GUI.get_all_buttons())):
                    for y in range(len(GUI.get_all_buttons()[x])):
                        GUI.get_all_buttons()[x][y].grid()
                        GUI.get_all_buttons()[x][y].configure(
                            state = 'normal'
                            )
                Gamelogic.__shipcount -= 1
                Gamelogic.__ships = list(set(Gamelogic.__ships))

        if Gamelogic.__shipcount < 0:
            GUI.all_ships_placed()

    def handle_shot(shot):
        shot = list(shot)
        shot.pop(0)
        for x in range(len(GUI.get_own_buttons())):
            for y in range(len(GUI.get_own_buttons()[x])):
                if (GUI.get_own_buttons()[x][y].data[0] == shot[0]) \
                    and (GUI.get_own_buttons()[x][y].data[1] == shot[1]):
                    GUI.get_own_buttons()[x][y].configure(bg='grey')
                    Gamelogic.__enemyshots.append(GUI.get_own_buttons()[x][y])
                    Gamelogic.__enemyshots = list(set(Gamelogic.__enemyshots))
                    Gamelogic.set_enemy_turn_to_False()
                    Gamelogic.check_for_hit(shot)
                    # Bug dass Knöpfe öfter in GUI.__get_own_buttons() stehen
                    if set(Gamelogic.__ships).issubset \
                        (Gamelogic.__enemyshots) and Gamelogic.__winner \
                        == False:
                        Gamelogic.__winner = True
                        GUI.tell_winner(0)
                        Network.send_data('won')

    def check_for_hit(shot):
        for i in range(len(Gamelogic.__ships)):
            if (Gamelogic.__ships[i].data[0] == shot[0]) \
                and (Gamelogic.__ships[i].data[1] == shot[1]):
                Network.send_hit()
                GUI.mark_own_hit(Gamelogic.__ships[i])

    def set_enemy_turn_to_False():
        Gamelogic.__enemies_turn = False

    def set_enemy_turn_to_True():
        Gamelogic.__enemies_turn = True

    def set_enemy_ready():
        Gamelogic.__enemy_ready = True

    def get_enemy_turn():
        return Gamelogic.__enemies_turn
    
    def give_shipsize():
        return Gamelogic.__shipcount

class Network:

    __client = None
    __HOST_PORT = 0
    __HOST_ADDRESS = ''

    def read_config():
        config = configparser.ConfigParser()
        config.read('serverconfig.ini')
        Network.__HOST_ADDRESS = config.get('SERVER', 'HOST_ADDRESS')
        Network.__HOST_PORT = config.get('SERVER', 'HOST_PORT')

    def connect_to_server():
        try:
            Network.__client = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            Network.__client.connect(
                (Network.__HOST_ADDRESS, int(Network.__HOST_PORT)))
            t = threading.Thread(
                target=Network.receive_message_from_server,
                    args=(Network.__client,))
            t.start()

        except:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(title='Connection Error',
                message='Cannot connect to server: ' + Network.__HOST_ADDRESS
                + ' on port: ' + str(Network.__HOST_PORT))
    
    def send_shot(data):
        if Gamelogic.__enemies_turn == False:
            Network.__client.send(pickle.dumps(data))
            Gamelogic.__enemies_turn = True
    
    def send_hit():
        Network.__client.send(pickle.dumps('hit'))
        Gamelogic.set_enemy_turn_to_True()

    def send_data(data):
        Network.__client.send(pickle.dumps(data))

    def receive_message_from_server(server_connection):

        while True:
            from_server = server_connection.recv(4096)

            if not from_server:
                break

            if from_server.startswith('welcome'.encode()):
                if from_server == 'welcome1'.encode():
                    GUI.welcome_player(1)
                    Gamelogic.set_enemy_turn_to_False()
                elif from_server == 'welcome2'.encode():
                    GUI.welcome_player(2)

            elif pickle.loads(from_server)[0] == 's':
                Gamelogic.handle_shot(pickle.loads(from_server))

            elif pickle.loads(from_server) == 'ready':
                Gamelogic.set_enemy_ready()

            elif pickle.loads(from_server) == 'hit':
                Gamelogic.set_enemy_turn_to_False()
                GUI.mark_enemy_hit()

            elif pickle.loads(from_server) == 'won':
                GUI.tell_winner(1)

if __name__ == '__main__':
    
    def start_game():
        Network.read_config()
        Network.connect_to_server()
        tk_window = tk.Tk()
        tk_window.title('Schiffe versenken')
        tk_window.protocol('WM_DELETE_WINDOW', on_closing)
        app = GUI(tk_window)
        app.mainloop()

    def on_closing():
        os._exit(0)

    t = threading.Thread(target = start_game())
    t.start()
