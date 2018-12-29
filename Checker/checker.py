class Checker:
    BOTTOM = 1
    TOP = 2
    BOTTOM_KING = 3
    TOP_KING = 4

    def __init__(self, type):
        self.type = type

    def king(self):
        if self.type == self.BOTTOM:
            self.type = self.BOTTOM_KING
        elif self.type == self.TOP:
            self.type = self.TOP_KING

    @property
    def is_king(self):
        return self.type == self.TOP_KING or self.type == self.TOP_KING
