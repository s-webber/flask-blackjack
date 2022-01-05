class BlackjackException(Exception):
    pass


class GameNotFoundException(BlackjackException):
    pass


class GameNotOpenException(BlackjackException):
    pass
