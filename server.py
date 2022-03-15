import zmq
import random

from file import *

class Server:
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    list_of_id = []
    db_files = []

    def __init__(self, url):
        self.socket.bind(url)

    def generate_identifier(self) ->  int:
        while True:
            new_id = random.randint(0,100)
            if new_id not in self.list_of_id:
                self.list_of_id.append(new_id)
                break
        return new_id

    def get_file(self, id_received: int):
        #function to obtain the corresponding file of each users
        for file in self.db_files:
            if id_received == file.id_user:
                return file

    def save_bd(self, id_user, file_name, size):
        rename_file_name = str(id_user) + '_' + file_name
        file = File(id_user, file_name, size, rename_file_name)
        self.db_files.append(file)

    def listen_requests(self):
        while True:
            content = self.socket.recv_multipart()
            if content[4].decode() == '0':
                #is requesting an identifier
                new_id = self.generate_identifier()
                self.save_bd(new_id, content[1].decode(), content[2].decode())
                self.socket.send_string(str(new_id))
                continue
            else:
                #already have an identifier and everything is already saved
                new_file : File = self.get_file(int(content[3].decode()))
                with open(new_file.rename_file, 'ab') as f:
                    f.write(content[0])
                    new_file.amount_saved += len(content[0])
                    if int(new_file.size) == new_file.amount_saved:
                        new_file.full = True
                        msg = f'your file{new_file.file_name} is uploaded to the server'
                        self.socket.send_string(msg)
                    else:
                        msg = f'your file{new_file.file_name} is not uploaded yet, size up:{new_file.amount_saved} bytes'
                        self.socket.send_string(msg)
            print(f'{new_file.id_user}, archive:{new_file.file_name}, file weight:{new_file.size}, '
                  f'size uploaded to server:{new_file.amount_saved}')

if __name__ == '__main__':
    Server(url='tcp://*:5555').listen_requests()