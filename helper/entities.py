import enum
 
class CommandType(enum.Enum):
    JOIN = 1
    PING = 2
    UPDATE_CONNECTIONS = 3
    CHANGE_DATASET = 4
    CLIENT_REQUEST = 5

class Command():
    def __init__(self, type: CommandType, args: dict) -> None:
        self.type = type
        self.args = args