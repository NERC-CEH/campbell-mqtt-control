from campbellcontrol.config import Config
from campbellcontrol.connection.aws import AWSConnection
from campbellcontrol.connection.generic import PahoConnection
from campbellcontrol.connection.interface import Connection
from campbellcontrol.control import AWSCommandHandler, CommandHandler, PahoCommandHandler


def get_connection(config: Config) -> Connection:
    """Reads the config and returns an appropriate Connection"""

    if config.broker.lower() == "aws":
        return AWSConnection(*config.connection_args(), **config.connection_options())
    else:
        return PahoConnection(*config.connection_args())
        # TODO implement mTLS with Paho, if we need it
        #                      **config.connection_options())


def get_command_handler(connection: Connection) -> CommandHandler:
    """Returns the right CommandHandler for the Connection"""
    if isinstance(connection, PahoConnection):
        return PahoCommandHandler(connection)
    elif isinstance(connection, AWSConnection):
        return AWSCommandHandler(connection)
    else:
        raise ValueError(f"Unknown connection type: {type(connection)}")
