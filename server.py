import tkinter as tk
import socket
import threading
import time
import configparser
import pickle
import ctypes
import os

class GUI(tk.Frame):

    __labels = []

    def __init__(self, master):
        ctypes.windll.user32.ShowWindow \
        (ctypes.windll.kernel32.GetConsoleWindow(), 0)
        super().__init__(master) 
        master.geometry('200x250') 
        self.f1 = tk.Frame(master = master)
        self.f1.pack(fill = tk.BOTH, expand = True)
        self.grid_length = 1
        self.grid_height = 3
        self.create_board()

        for x in range(self.grid_length):
            self.f1.columnconfigure(x, weight = 1)
        for y in range(self.grid_height):
            self.f1.rowconfigure(y, weight = 1)
    
    def create_board(self):
        for x in range(self.grid_length):
            for y in range(self.grid_height):
                l = tk.Label(master = self.f1, bg = 'white')
                l.grid(row = y, column = x, sticky = tk.N + tk.S + tk.E + tk.W)
                GUI.__labels.append(l)

    @staticmethod
    def get_labels():
        return GUI.__labels
    
class Network:

    # clients list is for remembering to which player send which
    # information at a specific time --> to alternate between the two players
    __server = None
    __HOST_PORT = 0
    __HOST_ADDRESS = ""
    __clients = []
    __players_connected = False

    @staticmethod
    def read_config():
        config = configparser.ConfigParser()
        config.read('serverconfig.ini')
        Network.__HOST_ADDRESS = config.get('SERVER', 'HOST_ADDRESS')
        Network.__HOST_PORT = config.get('SERVER', 'HOST_PORT')

    @staticmethod    
    def start_server():
        Network.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Network.__server.bind((Network.__HOST_ADDRESS,
            int(Network.__HOST_PORT)))
        Network.__server.listen(2)
        GUI.get_labels()[0].configure(text = 'Server running!', fg = 'black')
        t = threading.Thread(target = Network.accept_clients,
            args = (Network.__server,))
        t.start()

    @staticmethod        
    def accept_clients(started_server):
        GUI.get_labels()[2].configure(text = 'Now accepting Clients')
        while len(Network.__clients) < 2:
            client, address = started_server.accept()
            Network.__clients.append(client)
            t = threading.Thread(target = Network.send_startup_message, 
                args = (client,))
            t.start()

    @staticmethod
    def send_startup_message(client_connection):

        if len(Network.__clients) < 2:
            client_connection.send("welcome1".encode())
            GUI.get_labels()[1].configure(text = 'Player 1 connected!')
        else:
            client_connection.send("welcome2".encode())
            GUI.get_labels()[1].configure(text = 'Both Players connected')
            GUI.get_labels()[2].configure(text = '')
            Network.__players_connected = True

    @staticmethod
    def tell_if_ready():
        return Network.__players_connected

    @staticmethod
    def receive():
        while True:
            if Network.tell_if_ready() == True:
                for i in range(2):
                    t = threading.Thread(
                        target = Network.receive_message_from_client,
                        args = (i,)
                        )
                    t.start()
                break

    @staticmethod
    def receive_message_from_client(index):
        
        while True:
            from_client = Network.__clients[index].recv(4096)

            if not from_client:
                break   

            elif pickle.loads(from_client) == "ready":
                Network.send_data_to_enemy("ready", index)

            elif pickle.loads(from_client) == "hit":
                Network.send_data_to_enemy("hit", index)

            elif pickle.loads(from_client) == "won":
                Network.send_data_to_enemy("won", index)

            elif pickle.loads(from_client)[0] == "s":
                Network.convert_shot(pickle.loads(from_client), index)

    @staticmethod
    def convert_shot(shot, index):
        shot = list(shot)
        shot[2] += 11
        Network.send_data_to_enemy(tuple(shot), index)

    def send_data_to_enemy(data, player):
        if player == 0:
            Network.__clients[1].send(pickle.dumps(data))
        else:
            Network.__clients[0].send(pickle.dumps(data))

if __name__ == '__main__':

    def create_gui():
        tk_window = tk.Tk()
        tk_window.title('Schiffe versenken Server')
        tk_window.protocol("WM_DELETE_WINDOW", on_closing)
        app = GUI(tk_window)
        app.mainloop()
    
    def on_closing():
        os._exit(0)

    t = threading.Thread(target = create_gui)
    t.start()

    time.sleep(0.5)
    Network.read_config()
    Network.start_server()

    t = threading.Thread(target = Network.receive)
    t.start()  