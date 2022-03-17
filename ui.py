import os

class Ui:
    def __init__(self):
        pass

    @staticmethod
    def clear_console():
        command = 'clear'
        if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
            command = 'cls'
        os.system(command)

    @staticmethod
    def check_file_existence(path):
        return os.path.exists(path)

    @staticmethod
    def menu():
        start_menu = '''
        ---File System---
        1.Enter File
        2.Download file
        3.Exit
        Option:'''
        return start_menu