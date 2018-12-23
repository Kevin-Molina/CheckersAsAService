class Server:

    def __init__(self):
        self._usernames = set()
        self._players = []
        self._names_in_use = set()
        self._games = []

    def is_username_free(self, username):
        return username not in self._usernames
