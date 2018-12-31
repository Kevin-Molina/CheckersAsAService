from Board.board import Board
from Checker.checker import Checker
import random


class Game:
    def __init__(self, player_a, player_b):
        """Randomly pick a player to start as player_one that makes the first move
        By default, player_one starts at the bottom of the board"""
        self.board = Board()
        self.players_turn = random.choice((player_a, player_b))
        if self.players_turn is player_a:
            self.player_one = player_a
            self.player_two = player_b
        else:
            self.player_one = player_b
            self.player_two = player_a

    def do_turn(self, player, move):
        if not player or not move:
            raise Exception('Invalid move format')

        for i in move:
            if type(i) is not int:
                raise Exception('Invalid move format - Must be integers')

        if self.players_turn != player:
            raise Exception('Player can only move on turn')

        if player == self.player_one:
            if not self.board.player_owns_piece(move[0], [Checker.PLAYER_ONE, Checker.PLAYER_ONE_KING]):
                raise Exception('Player can only move their own piece')

        elif not self.board.player_owns_piece(move[0], [Checker.PLAYER_TWO, Checker.PLAYER_TWO_KING]):
            raise Exception('Player can only move their own piece')

        if not self.board.is_valid_move(move):
            raise Exception('Invalid move')

        else:
            if player == self.player_one:
                self.players_turn = self.player_two
            else:
                self.players_turn = self.player_one
            self.board.move(move)

    def get_opponent(self, player):
        if player == self.player_one:
            return self.player_two
        else:
            return self.player_one
