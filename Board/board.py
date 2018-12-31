from Checker.checker import Checker
from copy import deepcopy


class Board:
    def __init__(self):
        self.board = self._get_new_board()

    @staticmethod
    def _get_new_board():
        """Creates an empty board 3 rows at a time"""
        board = [None for _ in range(64)]
        player_one_index = 0
        player_two_index = 41
        for _ in range(4):
            board[player_one_index] = Checker(Checker.PLAYER_ONE)
            board[player_two_index] = Checker(Checker.PLAYER_TWO)
            player_one_index += 2
            player_two_index += 2

        player_one_index = 9
        player_two_index = 48
        for _ in range(4):
            board[player_one_index] = Checker(Checker.PLAYER_ONE)
            board[player_two_index] = Checker(Checker.PLAYER_TWO)
            player_one_index += 2
            player_two_index += 2

        player_one_index = 16
        player_two_index = 57
        for _ in range(4):
            board[player_one_index] = Checker(Checker.PLAYER_ONE)
            board[player_two_index] = Checker(Checker.PLAYER_TWO)
            player_one_index += 2
            player_two_index += 2

        return board

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

    @staticmethod
    def _is_valid_single_move(start, end, temp_board):

        # Indices not in bounds
        if start < 0 or start >= len(temp_board):
            return False

        if end < 0 or end >= len(temp_board):
            return False

        # End is not empty
        if temp_board[end]:
            return False
        print('hit1')
        start_piece = temp_board[start]

        # Verify movement directions are permitted
        if end-start > 0 and start_piece.type == Checker.PLAYER_TWO:
            return False

        if end-start < 0 and start_piece.type == Checker.PLAYER_ONE:
            return False

        dif = abs(end-start)

        # Single hop diagonal move
        if dif in [7, 9]:
            return True

        # Double hop diagonal move
        if dif in [14, 18]:
            midpoint = (start + end) // 2
            mid_piece = temp_board[midpoint]

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

    @staticmethod
    def _make_single_move(start, end, board):
        dif = abs(end-start)

        if dif in [7, 9]:
            board[end] = board[start]
            board[start] = None
        else:
            midpoint = (start + end) // 2
            board[end] = board[start]
            board[midpoint] = None
            board[start] = None

    def is_valid_move(self, move_list):

        temp_board = self._get_board_clone()

        for i in range(len(move_list) - 1):
            if not self._is_valid_single_move(move_list[i], move_list[i+1], temp_board):
                return False
            else:
                self._make_single_move(move_list[i], move_list[i+1], temp_board)
        return True

    def move(self, move_list):
        for i in range(len(move_list)-1):
            self._make_single_move(move_list[i], move_list[i+1], self.board)




