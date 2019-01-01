class Checker:
    PLAYER_ONE = 1
    PLAYER_TWO = 2
    PLAYER_ONE_KING = 3
    PLAYER_TWO_KING = 4

    def __init__(self, checker_type):
        self.type = checker_type

    def king(self):
        if self.type <= 2:
            self.type += 2

    @property
    def is_king(self):
        return self.type > 2

    @property
    def player_number(self):
        return self.type if self.type <= 2 else self.type - 2
