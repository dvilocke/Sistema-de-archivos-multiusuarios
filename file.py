class File:
    def __init__(self, id_user, file_name, size, amount_saved = 0 , full = False):
        self.id_user = id_user
        self.file_name = file_name
        self.size = size
        self.rename_file = str(self.id_user) + '_' + self.file_name
        self.amount_saved = amount_saved
        self.full = full

    def reset_values(self):
        self.size = 0
        self.amount_saved = 0
        self.full = False

    def __str__(self):
        return f'id_user:{self.id_user}, file_name:{self.file_name}, rename_file:{self.rename_file}, size:{self.size}, amount_saved:{self.amount_saved}, full:{self.full}'