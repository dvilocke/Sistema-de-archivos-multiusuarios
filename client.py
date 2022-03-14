import zmq
import os

class Client:

    SIZE = 1024*1024
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    def __init__(self, filename:str, url):
        self.filename = filename
        self.id = None
        self.socket.connect(url)

    def get_file_size(self) -> int:
        return os.path.getsize(self.filename)


    def save_file(self):
        #send necessary information
        self.socket.send_multipart(
            [''.encode(), self.filename.encode(), str(self.get_file_size()).encode(), ''.encode(), '0'.encode()]
        )
        self.id = self.socket.recv_string()
        print(self.id)

        '''

        while True:
            with open(self.filename, 'rb') as f:
                content = f.read(self.SIZE)
                if content:
                    while content:
                        self.socket.send_multipart(
                            [content, self.filename.encode(), '1'.encode()]
                        )
                        self.socket.recv().decode()
                        content = f.read(self.SIZE)

            self.socket.send_multipart([''.encode(), '1'.encode()])
            print(self.socket.recv().decode())
            break
        '''

if __name__ == '__main__':
    Client(filename='cosa.txt', url='tcp://localhost:5555').save_file()