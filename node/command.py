from enum import Enum

class Commands(Enum):
    PUT = "PUT"
    GET = "GET"

    @staticmethod
    def argument_count():
        return {
            Commands.PUT: 2,  # Example: PUT requires 2 arguments
            Commands.GET: 1   # Example: GET requires 1 argument
        }

def is_valid_command(command_string: str) -> False:
    parts = command_string.split()
    if not parts:
        return False
    
    command_name, *args = parts
    try:
        command = Commands[command_name]
    except KeyError:
        return False

    expected_arg_count = Commands.argument_count().get(command, 0)
    return len(args) == expected_arg_count