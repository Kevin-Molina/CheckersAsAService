import json


class Messages:
    INVALID_USERNAME = json.dumps(
        {"usernameValid": False}
    )

    VALID_USERNAME = json.dumps(
        {"usernameValid": True}
    )

    ESTIMATED_WAIT_TIME = json.dumps(
        {"estimatedWait": "< 1 minute"}
    )

    OPPONENT_DISCONNECTED = json.dumps(
        {"opponentDisconnected": True}
    )

    VALID_MOVE = json.dumps(
        {"validMove": True}
    )

    INVALID_MOVE = json.dumps(
        {"validMove": False}
    )

    @staticmethod
    def create_invitation(challenger):
        return json.dumps(
            {"challengingPlayer": challenger}
        )

    @staticmethod
    def game_start(opponent, first_move):
        return json.dumps(
            {"matchStart": True,
             "opponent": opponent,
             "firstMove": first_move}
        )

    @staticmethod
    def move(move):
        return json.dumps(
            {"move": move}
        )

    @staticmethod
    def winnner(winner_name):
        return json.dumps(
            {"winner": winner_name}
        )