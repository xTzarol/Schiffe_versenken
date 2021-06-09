import tkinter as tk
import socket
import threading
import time
import configparser
import pickle

class GUI(tk.Frame):

    labels = []

    def __init__(self, master):
        super().__init__(master) 
        master.geometry('200x250') 
        #frame
        self.f1 = tk.Frame(master=master)
        self.f1.pack(fill=tk.BOTH, expand=True)
        self.grid_length = 1
        self.grid_height = 3
        self.create_board()

        for x in range(self.grid_length):
            self.f1.columnconfigure(x, weight=1)
        for y in range(self.grid_height):
            self.f1.rowconfigure(y, weight=1)
    
    def create_board(self):
        for x in range(self.grid_length):
            for y in range(self.grid_height):
                l = tk.Label(master=self.f1, bg = 'white', text = "hello")
                l.grid(row=y, column=x, sticky=tk.N+tk.S+tk.E+tk.W)
                GUI.labels.append(l)
    
class Network:

    #clients list is for remembering to which player send which information at a specific time --> to alternate between the two players
    __server = None
    __HOST_PORT = 0
    __HOST_ADDRESS = ""
    __clients = []
    __players_connected = False
   
    def read_config():
        config = configparser.ConfigParser()
        config.read('serverconfig.ini')
        Network.__HOST_ADDRESS = config.get('SERVER', 'HOST_ADDRESS')
        Network.__HOST_PORT = config.get('SERVER', 'HOST_PORT')
    
    def start_server():
        Network.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Network.__server.bind((Network.__HOST_ADDRESS, int(Network.__HOST_PORT)))
        Network.__server.listen(2)
        GUI.labels[0].configure(text = 'Server started!', fg = 'black')
        t = threading.Thread(target = Network.accept_clients, args = (Network.__server, ))
        t.start()
        
    def accept_clients(started_server):
        print("Now accepting clients!")
        while len(Network.__clients) < 2:
            client, address = started_server.accept()
            Network.__clients.append(client)
            t = threading.Thread(target = Network.send_startup_message, args = (client, address))
            t.start()

    def send_startup_message(client_connection, ip_address):

        if len(Network.__clients) < 2:
            client_connection.send("welcome1".encode())
            print("Connection from", client_connection.getpeername(),"successful!")
        else:
            client_connection.send("welcome2".encode())
            print("Connection from", client_connection.getpeername(),"successful!")
            Network.__players_connected = True

    def tell_if_ready():
        return Network.__players_connected

    def receive_message_from_client(index):
        
        while True:
            from_client = Network.__clients[index].recv(4096)

            if not from_client:
                break   

            elif pickle.loads(from_client) == "ready":
                Network.send_data_to_enemy("ready", index)
                    
            elif isinstance(pickle.loads(from_client), tuple) == True:
                Network.convert_shot(pickle.loads(from_client), index)

            elif pickle.loads(from_client) == "hit":
                Network.send_data_to_enemy("hit", index)

#Einfügen dass Spieler der gerade an der Reihe ist übergeben wird damit auf richtige Verbindung gehorcht bzw. von richtiger Verbindung empfangen wird
    def convert_shot(shot, index):
        shot = list(shot)
        shot[1] += 11
        Network.send_data_to_enemy(tuple(shot), index)

    def send_data_to_enemy(data, player):
        if player == 0:
            Network.__clients[1].send(pickle.dumps(data))
        if player == 1:
            Network.__clients[0].send(pickle.dumps(data))

    def print_server():
        server_stats = []
        server_stats.append(Network.__HOST_ADDRESS)
        server_stats.append(Network.__HOST_PORT)
        return server_stats
    
    def get_number_of_clients():
        return len(Network.__clients)

if __name__ == '__main__':

    def create_gui():
        tk_window = tk.Tk()
        tk_window.title('Schiffe versenken Server')
        app = GUI(tk_window)
        app.mainloop()

    def receive():
        while True:
            if Network.tell_if_ready() == True:
                for i in range(2):
                    t = threading.Thread(target = Network.receive_message_from_client, args = (i, ))
                    t.start()
                break

    t = threading.Thread(target = create_gui)
    t.start()

    time.sleep(1)
    Network.read_config()
    Network.start_server()

    t = threading.Thread(target = receive)
    t.start()  
            
    #tk_window = tk.Tk()
    #tk_window.title('Schiffe versenken Server')
    #app = GUI(tk_window)
    #app.mainloop()
