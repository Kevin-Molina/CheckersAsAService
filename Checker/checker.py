class Checker:
    PLAYER_ONE = 1
    PLAYER_TWO = 2
    PLAYER_ONE_KING = 3
    PLAYER_TWO_KING = 4

    def __init__(self, checker_type):
        self.type = checker_type

    def king(self):
        if self.type == self.PLAYER_ONE:
            self.type = self.PLAYER_ONE_KING
        elif self.type == self.PLAYER_TWO:
            self.type = self.PLAYER_TWO_KING

    @property
    def is_king(self):
        return self.type == self.PLAYER_ONE_KING or self.type == self.PLAYER_TWO_KING
