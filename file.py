class File:
    def __init__(self, id_user, file_name, size, rename_file, amount_saved = 0 , full = False):
        self.id_user = id_user
        self.file_name = file_name
        self.size = size
        self.rename_file = rename_file
        self.amount_saved = amount_saved
        self.full = full

    def __str__(self):
        return f'id_user:{self.id_user}, file_name:{self.file_name}, size:{self.size}, amount_saved:{self.amount_saved}, full:{self.full}'