import zmq
import random
import os
from file import *

class Server:
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    db_users = {}

    def __init__(self, url):
        self.socket.bind(url)

    def generate_identifier(self) ->  int:
        while True:
            new_id = random.randint(0,100)
            if new_id not in self.db_users:
                self.db_users[new_id] = []
                break
        return new_id

    def check_existence(self, id_received:int, filename : str):
        for file in self.db_users[id_received]:
            if file.file_name == filename:
                return file
        return None


    def listen_requests(self):
        while True:
            content = self.socket.recv_multipart()
            if content[5].decode() == '0':
                #is requesting an identifier
                new_id = self.generate_identifier()
                self.socket.send_string(str(new_id))
                continue
            else:
                #already have an identifier and everything is already saved
                new_file : File = self.check_existence(int(content[4].decode()), content[1].decode())
                if new_file is None:
                    #the file is new
                    file = File(int(content[4].decode()), content[1].decode(), int(content[2].decode()))
                    self.db_users[int(content[4].decode())].append(file)
                    new_file = self.check_existence(int(content[4].decode()), content[1].decode())
                else:
                    if new_file.full:
                        #if the file is full it means it is an overwrite
                        new_file.reset_values()
                        new_file.size = int(content[2].decode())
                        os.remove(new_file.rename_file)
                        print(f'{new_file.id_user}, is overwriting the file:{new_file.file_name}')


                with open(new_file.rename_file, 'ab') as f:
                    f.write(content[0])
                    new_file.amount_saved += len(content[0])
                    if int(new_file.size) == new_file.amount_saved:
                        new_file.full = True
                        msg = f'your file{new_file.file_name} is uploaded to the server, size up:{new_file.amount_saved} bytes'
                        self.socket.send_string(msg)
                    else:
                        msg = f'your file{new_file.file_name} is not uploaded yet, size up:{new_file.amount_saved} bytes'
                        new_file.full = False
                        self.socket.send_string(msg)

            print(f'{new_file.id_user}, archive:{new_file.file_name}, file weight:{new_file.size}, '
                  f'size uploaded to server:{new_file.amount_saved}')

if __name__ == '__main__':
    Server(url='tcp://*:5555').listen_requests()