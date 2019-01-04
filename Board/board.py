from Checker.checker import Checker
from copy import deepcopy


class Board:
    PLAYER_ONE_ROW_STARTS = [40, 49, 56]
    PLAYER_TWO_ROW_STARTS = [1, 8, 17]

    # [00, 01, 02, 03, 04, 05, 06, 07]
    # [08, 09, 10, 11, 12, 13, 14, 15]
    # [16, 17, 18, 19, 20, 21, 22, 23]
    # [24, 25, 26, 27, 28, 29, 30, 31]
    # [32, 33, 34, 35, 36, 37, 38, 39]
    # [40, 41, 42, 43, 44, 45, 46, 47]
    # [48, 49, 50, 51, 52, 53, 54, 55]
    # [56, 57, 58, 59, 60, 61, 62, 63]

    def __init__(self):
        self.board = self._get_new_board()
        self.checker_counts = {Checker.PLAYER_ONE: 12,
                               Checker.PLAYER_TWO: 12}

    def _get_new_board(self):
        """Creates an empty board 3 rows at a time"""
        board = [None for _ in range(64)]

        for board_index in self.PLAYER_ONE_ROW_STARTS:
            self._set_row(board, board_index, Checker.PLAYER_ONE)

        for board_index in self.PLAYER_TWO_ROW_STARTS:
            self._set_row(board, board_index, Checker.PLAYER_TWO)

        return board

    @staticmethod
    def _set_row(board, start_index, piece):
        board[start_index:start_index + 8:2] = [Checker(piece) for _ in range(4)]

    def player_owns_piece(self, index, player_number):
        return self.board[index].player_number == player_number

    @staticmethod
    def _get_checker_row(index):
        return index // 8

    def _is_valid_single_move(self, start, end):

        # Indices not in bounds
        if start < 0 or start >= len(self.board):
            return False

        if end < 0 or end >= len(self.board):
            return False

        # End is not empty
        if self.board[end]:
            return False

        start_piece = self.board[start]

        if not start_piece:
            return False

        # Verify movement directions are permitted
        if end-start > 0 and start_piece.type == Checker.PLAYER_ONE:
            return False

        if end-start < 0 and start_piece.type == Checker.PLAYER_TWO:
            return False

        dif = abs(end-start)

        # Single hop diagonal move
        if dif in [7, 9]:
            # Prevent movement wrapping around the sides
            if abs(self._get_checker_row(start) - self._get_checker_row(end)) != 1:
                return False
            return True

        # Double hop diagonal move
        if dif in [14, 18]:
            midpoint = (start + end) // 2
            mid_piece = self.board[midpoint]

            if not mid_piece:
                return False

            # Prevent movement wrapping around the sides
            if abs(self._get_checker_row(start) - self._get_checker_row(end)) != 2:
                return False

            # Verify the hopped piece is of opposite color
            if start_piece.player_number != mid_piece.player_number:
                return True
            else:
                return False

        else:
            return False

    def _make_single_move(self, start, end):
        dif = abs(end-start)

        if dif in [7, 9]:
            self.board[end] = self.board[start]
            self.board[start] = None
        else:
            midpoint = (start + end) // 2
            self.board[end] = self.board[start]
            self.board[midpoint] = None
            self.board[start] = None

        if 0 >= end <= 7 or 56 >= end <= 63:
            self._king(end)

    def _king(self, piece_index):
        checker = self.board[piece_index]
        checker.king()

    def move(self, move_list):
        backup_board = deepcopy(self.board)
        backup_checker_counts = deepcopy(self.checker_counts)
        invalid_move_found = False

        for move_pair in move_list:
            if self._is_valid_single_move(move_pair[0], move_pair[1]):
                self._make_single_move(move_pair[0], move_pair[1])
            else:
                self.board = backup_board
                self.checker_counts = backup_checker_counts
                raise Exception

    def has_moves_left(self, player_num):
        if not self.checker_counts[player_num]:
            return False
        has_move_left = False

        for idx, checker in enumerate(self.board):
            if checker and checker.player_number == player_num and self._get_valid_moves(idx):
                has_move_left = True
                break
        return has_move_left

    def _get_valid_moves(self, checker_index):
        valid_moves = []
        if self._is_valid_single_move(checker_index, checker_index + 7):
            valid_moves.append((checker_index, checker_index + 7))
        if self._is_valid_single_move(checker_index, checker_index - 7):
            valid_moves.append((checker_index, checker_index - 7))
        if self._is_valid_single_move(checker_index, checker_index + 9):
            valid_moves.append((checker_index, checker_index + 9))
        if self._is_valid_single_move(checker_index, checker_index - 9):
            valid_moves.append((checker_index, checker_index - 9))
        if self._is_valid_single_move(checker_index, checker_index + 14):
            valid_moves.append((checker_index, checker_index + 14))
        if self._is_valid_single_move(checker_index, checker_index - 14):
            valid_moves.append((checker_index, checker_index - 14))
        if self._is_valid_single_move(checker_index, checker_index + 18):
            valid_moves.append((checker_index, checker_index + 18))
        if self._is_valid_single_move(checker_index, checker_index - 18):
            valid_moves.append((checker_index, checker_index - 18))

        return valid_moves
