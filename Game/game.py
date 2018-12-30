from Board.board import Board
from Checker.checker import Checker
import random


class Game:
    def __init__(self, player_one, player_two):
        self.board = Board()
        self.player_one = player_one
        self.player_two = player_two
        self.players_turn = random.choice((self.player_one, self.player_two))

    def do_turn(self, player, moves):
        if not player or not moves:
            # error
            pass

        if self.players_turn != player:
            # error
            pass

        for i in moves:
            if i is not int:
                # error
                pass

    def _move(self, start, end):
        pass
