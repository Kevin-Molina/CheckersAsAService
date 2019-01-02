from Board.board import Board
import random


class Game:
    def __init__(self, player_a, player_b):
        """Randomly pick a player to start as player_one that makes the first move
        By default, player_one starts at the bottom of the board"""
        self.board = Board()
        self.players = random.shuffle([player_a, player_b])
        self.players_turn = self.players[0]

    def do_turn(self, player, move):
        if not player or not move:
            raise Exception

        for i in move:
            if type(i) is not int:
                raise Exception

        if self.players_turn != player:
            raise Exception

        start_location = move[0]

        # Player[0] is (player 1)
        player_number = self.players.index(player) + 1

        if not self.board.player_owns_piece(start_location, player_number):
            raise Exception

        formatted_move = self._get_formatted_move(move)

        if not self.board.is_valid_move(formatted_move):
            raise Exception

        try:
            self.board.move(formatted_move)
        except:
            raise Exception

        if self.players_turn == self.players[0]:
            self.players_turn = self.players[1]
        else:
            self.players_turn = self.players[0]

    def get_opponent(self, player):
        if player == self.player_one:
            return self.player_two
        else:
            return self.player_one

    @staticmethod
    def _get_formatted_move(move):
        formatted_move = []
        for i in range(len(move) - 1):
            formatted_move.append((move[i], move[i+1]))
        return formatted_move
