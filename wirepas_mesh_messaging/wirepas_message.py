"""
    Wirpas message
    ===================

    .. Copyright:
        Copyright 2024 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""

from abc import ABC, abstractmethod

from .proto import GenericMessage
from .wirepas_exceptions import GatewayAPIParsingException, InvalidMessageType


class WirepasMessage(ABC):
    """
    An abstract base class used for interacting with Wirepas messages. Wirepas
    messages are protobuf messages which include a message under
    GenericMessage::wirepas.
    """

    @property
    @abstractmethod
    def payload(self):
        """
        The implementation should serialize the message and return the payload
        bytes.
        """

        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def _get_related_message(generic_message):
        """
        The implementation should return the relevant protobuf message
        contained under GenericMessage::wirepas.

        Parameters:
            - generic_message: Decoded GenericMessage object
        """

        raise NotImplementedError()

    @classmethod
    def _decode_and_get_related_message(cls, payload):
        """
        Decodes the given protobuf payload and returns the object to the
        relevant Wirepas message stored under GenericMessage::wirepas.

        Parameters:
            - payload: Payload of the encoded protobuf message

        Raises:
            - GatewayAPIParsingException
        """

        generic_message = GenericMessage()
        try:
            generic_message.ParseFromString(payload)
        except Exception as e:
            # Any Exception is promoted to Generic API exception
            raise GatewayAPIParsingException(
                "Cannot decode GenericMessage from payload"
            ) from e

        contained_message = cls._get_related_message(generic_message)

        # Works by checking if all required fields of contained_message are
        # set. In our case, every message holds a required header field.
        if not contained_message.IsInitialized():
            raise InvalidMessageType(
                f"Could not find relevant Wirepas message for {cls.__name__}"
            )

        return contained_message
