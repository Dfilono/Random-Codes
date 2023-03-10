import socket
from _thread import *
import pickle
from game import Game

server = "PUT IPV4 ADDRESS FOR LOCALHOST HERE"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))

except socket.error as e:
    print(e)

s.listen(2)
print("Waiting for a connect, Server Started")

connected = set()
games = {}
idCount = 0

def threaded_client(conn, p, gameID):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ''

    while True:
        try:
            data = conn.recv(4096).decode()

            if gameID in games:
                game = games[gameID]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()

                    elif data != "get":
                        game.play(p, data)

                    #reply = game
                    conn.sendall(pickle.dumps(game))

            else:
                break
        
        except:
            break

    print("Lost connect")
    try:
        del games[gameID]
        print("Closing game", gameID)
    
    except:
        pass

    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameID = (idCount - 1) // 2

    if idCount % 2 == 1:
        games[gameID] = Game(gameID)
        print("Creating a new game...")
    
    else:
        games[gameID].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameID))
