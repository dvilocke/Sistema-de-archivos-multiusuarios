import zmq

class Client:

    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    def __init__(self, filename, url):
        self.filename = filename
        self.id = None
        self.socket.connect(url)

    def save_file(self):
        self.socket.send_multipart([''.encode(), ''.encode(), '0'.encode()])
        self.id = self.socket.recv_string()
        print(self.id)

if __name__ == '__main__':
    Client(filename='cosa.txt', url='tcp://localhost:5555').save_file()