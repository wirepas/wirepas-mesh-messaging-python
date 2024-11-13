"""
    Set scratchpad target
    =====================

    .. Copyright:
        Copyright 2020 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""

from wirepas_mesh_messaging.wirepas_exceptions import InvalidMessageContents
from .proto import GenericMessage

from .request import Request
from .response import Response

from .otap_helper import (
    set_scratchpad_target,
    parse_scratchpad_target,
)


class SetScratchpadTargetAndActionRequest(Request):
    """
    SetScratchpadTargetAndActionRequest: request to set target scratchpad and action of a given sink

    Attributes:
        sink_id (str): id of the sink (dependant on gateway)
        target(dic): dictionary containing target scratchpad and associated action
            Dict keys are:
                action (ScratchpadAction): target action for network
                target_sequence (int): target sequence
                target_crc (int): target crc
                param(int): raw parameter for action
                delay(ProcessingDelay): delay for WITH_DELAY action
        req_id (int): unique request id
    """

    def __init__(self,
                 sink_id,
                 target,
                 req_id=None,
                 **kwargs):
        super(SetScratchpadTargetAndActionRequest, self).__init__(sink_id, req_id, **kwargs)

        if target["action"].value > 255:
            raise ValueError("Wrong Target action")

        try:
            seq = target["target_sequence"]
            if seq is not None and seq > 255:
                raise ValueError("Wrong Target sequence")
        except KeyError:
            # Key is optional
            pass

        try:
            crc = target["target_crc"]
            if crc is not None and crc > 0xffff:
                raise ValueError("Wrong Target crc")
        except KeyError:
            # Key is optional
            pass

        try:
            param = target["param"]
            if param is not None and param > 255:
                raise ValueError("Wrong Action param")
        except KeyError:
            # Key is optional
            pass

        try:
            delay = target["delay"]
            if delay is not None and delay.value > 255:
                raise ValueError("Wrong Action param")
        except KeyError:
            # Key is optional
            pass

        self.target = target

    @staticmethod
    def _get_related_message(generic_message):
        return generic_message.wirepas.set_scratchpad_target_and_action_req

    @classmethod
    def from_payload(cls, payload):
        req = cls._decode_and_get_related_message(payload)

        header = Request._parse_request_header(req.header)

        target = {}
        parse_scratchpad_target(req.target_and_action, target)

        try:
            return cls(
                sink_id=header["sink_id"],
                target=target,
                req_id=header["req_id"],
                time_ms_epoch=header["time_ms_epoch"],
            )
        except ValueError as e:
            raise InvalidMessageContents(
                f"Invalid values in {cls.__name__}", header
            ) from e

    @property
    def payload(self):
        message = GenericMessage()
        # Fill the request header
        req = self._get_related_message(message)
        self._load_request_header(req)

        set_scratchpad_target(req.target_and_action, self.target)

        return message.SerializeToString()


class SetScratchpadTargetAndActionResponse(Response):
    """
    SetScratchpadTargetAndActionResponse: Response to answer a SetScratchpadTargetAndActionRequest

      Attributes:
         req_id (int): unique request id that this Response is associated
         gw_id (str): gateway unique identifier
         res (GatewayResultCode): result of the operation
         sink_id (str): id of the sink (dependant on gateway)
     """

    def __init__(self, req_id, gw_id, res, sink_id, **kwargs):
        super(SetScratchpadTargetAndActionResponse, self).__init__(req_id, gw_id, res, sink_id, **kwargs)

    @staticmethod
    def _get_related_message(generic_message):
        return generic_message.wirepas.set_scratchpad_target_and_action_resp

    @classmethod
    def from_payload(cls, payload):
        response = cls._decode_and_get_related_message(payload)

        d = Response._parse_response_header(response.header)

        return cls(d["req_id"], d["gw_id"], d["res"], d["sink_id"], time_ms_epoch=d["time_ms_epoch"])

    @property
    def payload(self):
        message = GenericMessage()

        response = self._get_related_message(message)
        self._load_response_header(response)

        return message.SerializeToString()
