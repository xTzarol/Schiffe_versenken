import tkinter as tk
import socket
import threading
import time
import configparser
import sys
import ctypes
import pickle

class Network:

    #clients list is for remembering to which player send which information at a specific time --> to alternate between the two players
    __server = None
    __HOST_PORT = 0
    __HOST_ADDRESS = ""
    __clients = []
   
    def read_config():
        config = configparser.ConfigParser()
        config.read('serverconfig.ini')
        Network.__HOST_ADDRESS = config.get('SERVER', 'HOST_ADDRESS')
        Network.__HOST_PORT = config.get('SERVER', 'HOST_PORT')
    
    def start_server():
        Network.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Network.__server.bind((Network.__HOST_ADDRESS, int(Network.__HOST_PORT)))
        Network.__server.listen(2)
        print("Server started!")
        t = threading.Thread(target = Network.accept_clients, args = (Network.__server, ))
        t.start()
        
    def accept_clients(started_server):
        print("Now accepting clients!")
        while len(Network.__clients) < 2:
            client, address = started_server.accept()
            Network.__clients.append(client)
            t = threading.Thread(target = Network.send_startup_message, args = (client, address))
            t.start()

    def send_startup_message(client_connection, client_ip_address):

        if len(Network.__clients) < 2:
            client_connection.send("welcome1".encode())
            print("Connection from", client_connection.getpeername(),"successful!")
        else:
            client_connection.send("welcome2".encode())
            print("Connection from", client_connection.getpeername(),"successful!")

#Einfügen dass Spieler der gerade an der Reihe ist übergeben wird damit auf richtige Verbindung gehorcht bzw. von richtiger Verbindung empfangen wird
    def receive_shot():
        shot = list(pickle.loads(Network.__clients[0].recv(4096)))
        shot[1] += 11
        Network.send_shot(tuple(shot))

    def send_shot(shot):
        Network.__clients[1].send(pickle.dumps(shot))

    def receive_ready():
        return

    def print_server():
        server_stats = []
        server_stats.append(Network.__HOST_ADDRESS)
        server_stats.append(Network.__HOST_PORT)
        return server_stats
    
    def get_number_of_clients():
        return len(Network.__clients)

#class Gamelogic:

    #def serverlogic()     

if __name__ == '__main__':

    Network.read_config()
    Network.start_server()
    if sys.platform == 'win32':
        ctypes.windll.kernel32.SetConsoleTitleW("Schiffe versenken Server on {}:{}".format(Network.print_server()[0], Network.print_server()[1]))
    elif sys.platform == 'linux':
        print(f'\33]0;{title}\a', end='', flush=True)
    while True:
        if Network.get_number_of_clients() == 2:
            Network.receive_shot()
            
    #tk_window = tk.Tk()
    #tk_window.title('Schiffe versenken Server')
    #app = GUI(tk_window)
    #app.mainloop()
