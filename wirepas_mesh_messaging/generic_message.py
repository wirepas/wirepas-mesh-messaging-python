"""
    Generic message
    ========
    .. Copyright:
        Copyright 2022 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""


from .wirepas_exceptions import GatewayAPIParsingException
from .proto import GenericMessage as protoGenericMessage


class GenericMessage(object):
    """
    Generic message
    Base class for all Events, Requests, Response
    """

    @classmethod
    def from_generic_message(cls, message):
        """ Implement how to parse message """
        raise NotImplementedError()

    @classmethod
    def from_payload(cls, payload):
        message = protoGenericMessage()
        try:
            message.ParseFromString(payload)
        except Exception:
            # Any Exception is promoted to Generic API exception
            raise GatewayAPIParsingException(
                "Cannot parse payload for %s" % cls.__name__
            )

        return cls.from_generic_message(message)

    def load_generic_message(self, message):
        """ Implement how to load generic message"""
        raise NotImplementedError()

    @property
    def payload(self):
        message = protoGenericMessage()
        return self.load_generic_message(message).SerializeToString()

    def __str__(self):
        return str(self.__dict__)