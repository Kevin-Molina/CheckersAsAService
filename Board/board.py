from Checker.checker import Checker
from copy import deepcopy


class Board:
    def __init__(self):
        self.board = [None for _ in range(64)]
        self.board[0:24:2] = [Checker(Checker.PLAYER_ONE) for _ in range(12)]
        self.board[40:64:2] = [Checker(Checker.PLAYER_TWO) for _ in range(12)]

    def _reset_board(self):
        """Resets the board 3 rows at a time"""
        player_one_index = 0
        player_two_index = 41
        for _ in range(4):
            self.board[player_one_index] = Checker(Checker.PLAYER_ONE)
            self.board[player_two_index] = Checker(Checker.PLAYER_TWO)
            player_one_index += 2
            player_two_index += 2

        player_one_index = 9
        player_two_index = 48
        for _ in range(4):
            self.board[player_one_index] = Checker(Checker.PLAYER_ONE)
            self.board[player_two_index] = Checker(Checker.PLAYER_TWO)
            player_one_index += 2
            player_two_index += 2

        player_one_index = 16
        player_two_index = 57
        for _ in range(4):
            self.board[player_one_index] = Checker(Checker.PLAYER_ONE)
            self.board[player_two_index] = Checker(Checker.PLAYER_TWO)
            player_one_index += 2
            player_two_index += 2


    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63]

    # [56, 57, 58, 59, 60, 61, 62, 63]
    # [48, 49, 50, 51, 52, 53, 54, 55]
    # [40, 41, 42, 43, 44, 45, 46, 47]
    # [32, 33, 34, 35, 36, 37, 38, 39]
    # [24, 25, 26, 27, 28, 29, 30, 31]
    # [16, 17, 18, 19, 20, 21, 22, 23]
    # [08, 09, 10, 11, 12, 13, 14, 15]
    # [00, 01, 02, 03, 04, 05, 06, 07]

    def player_owns_piece(self, index, checker_types):
        return self.board[index].type in checker_types

    def _get_board_clone(self):
        return deepcopy(self.board)

    def is_valid_move(self, start, end):

        # Indices in bounds
        if start < 0 or start >= len(self.board):
            return False

        if end < 0 or end >= len(self.board):
            return False

        # End is empty
        if not self.board[end]:
            return False

        start_piece = self.board[start].type

        # Verify movement directions are permitted
        if end-start > 0 and (start_piece != Checker.PLAYER_TWO_KING or start_piece != Checker.PLAYER_ONE):
            return False

        if end-start < 0 and (start_piece != Checker.PLAYER_TWO or start_piece != Checker.PLAYER_ONE_KING):
            return False

        dif = abs(end-start)

        # Single hop diagonal move
        if dif in [7, 9]:
            return True

        # Double hop diagonal move
        if dif in [14, 18]:
            midpoint = (start + end) // 2
            mid_piece = self.board[midpoint]

            # Verify the hopped piece is of opposite color
            if start_piece.type == Checker.PLAYER_ONE or start_piece.type == Checker.PLAYER_ONE_KING:
                if mid_piece.type != Checker.PLAYER_TWO or mid_piece.type == Checker.PLAYER_TWO_KING:
                    return False

            if start_piece.type == Checker.PLAYER_TWO or start_piece.type == Checker.PLAYER_TWO_KING:
                if mid_piece.type != Checker.PLAYER_ONE or mid_piece.type != Checker.PLAYER_ONE_KING:
                    return False

            return True

        else:
            return False

    def move(self, begin, end):
        pass



