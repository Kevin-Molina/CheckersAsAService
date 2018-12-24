import json


class Messages:
    INVALID_USERNAME = json.dumps(
        {"usernameValid": False}
    )

    VALID_USERNAME = json.dumps(
        {"usernameValid": True}
    )

    @staticmethod
    def create_invitation(challenger):
        return json.dumps(
            {"challengingPlayer": challenger}
        )