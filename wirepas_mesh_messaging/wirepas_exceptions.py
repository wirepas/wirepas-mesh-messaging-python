"""
    Wirepas exceptions
    ==================

    .. Copyright:
        Copyright 2019 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""


class GatewayAPIParsingException(Exception):
    """
    Wirepas Gateway API generic Exception
    """

class InvalidMessageType(GatewayAPIParsingException):
    """
    Exception indicating wrong message type during deserialization
    """

class InvalidMessageContents(GatewayAPIParsingException):
    """
    Exception indicating invalid message contents in the received message.

    Parameters:
        - message: The exception message
        - header: Parsed header of the message, as a dictionary
    """

    def __init__(self, message, header):
        super().__init__(message)
        self.header = header
