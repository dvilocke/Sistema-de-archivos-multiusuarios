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

    def save_bd(self, id_user, file_name, size):
        file = File(id_user, file_name, size)
        self.db_files.append(file)

    def listen_requests(self):
        while True:
            content = self.socket.recv_multipart()
            if content[4].decode() == '0':
                #is requesting an identifier
                new_id = self.generate_identifier()
                self.save_bd(new_id, content[1].decode(), content[2].decode())
                self.socket.send_string(str(new_id))
                print(self.db_files[0])
                continue
            else:
                #already have an identifier
                pass
        pass



if __name__ == '__main__':
    Server(url='tcp://*:5555').listen_requests()