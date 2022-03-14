import zmq
import random

class Server:
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    list_of_id = []

    def __init__(self, url):
        self.socket.bind(url)

    def generate_identifier(self) ->  str:
        while True:
            new_id = random.randint(0,100)
            if new_id not in self.list_of_id:
                self.list_of_id.append(new_id)
                break
        return  str(new_id)

    def listen_requests(self):
        while True:
            content = self.socket.recv_multipart()
            if content[2].decode() == '0':
                #is requesting an identifier
                self.socket.send_string(self.generate_identifier())
                continue
            else:
                #already have an identifier
                pass
        pass



if __name__ == '__main__':
    Server(url='tcp://*:5555').listen_requests()