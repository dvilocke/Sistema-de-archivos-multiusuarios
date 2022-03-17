import zmq
import time
from ui import *

class Client:

    SIZE = 1024
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
        if self.id is None:
            self.socket.send_multipart(
                [''.encode(), self.filename.encode(), str(self.get_file_size()).encode(), ''.encode() ,''.encode(), '0'.encode()]
            )
            self.id = int(self.socket.recv_string())

        Ui.clear_console()
        print(f'\nYour Id is:{self.id}')
        print(f'file name:{self.filename}')
        print(f'File size:{self.get_file_size()}\n')

        while True:
            with open(self.filename, 'rb') as f:
                content = f.read(self.SIZE)
                if content:
                    while content:
                        self.socket.send_multipart(
                            [content, self.filename.encode(), str(self.get_file_size()).encode(), str(len(content)).encode(), str(self.id).encode(), '1'.encode()]
                        )
                        print(self.socket.recv_string())
                        content = f.read(self.SIZE)
            break

        print('\nprocess completed successfully')
        time.sleep(15)

if __name__ == '__main__':
    create_object = False
    client = None
    while True:
        Ui.clear_console()
        print(Ui.menu(), end='')
        option = int(input())
        if option == 1:
            file_name = input('\nEnter file name:')
            if Ui.check_file_existence(file_name):
                if not create_object:
                    client = Client(filename='', url='tcp://localhost:5555')
                    create_object = True

                client.filename = file_name
                client.save_file()
            else:
                print(f'\nThe file:{file_name} does not exists')
                time.sleep(4)
        elif option == 2:
            if client is not None:
                pass
            else:
                print(f'\nThe file:{file_name} does not exists')
                time.sleep(4)
        elif option == 3:
            break

    print('\nSee you soon')


