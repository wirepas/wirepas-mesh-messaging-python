"""
    Get scratchpad status
    =====================

    .. Copyright:
        Copyright 2019 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""

from .proto import GenericMessage

from .request import Request
from .response import Response

from .otap_helper import (
    set_scratchpad_info,
    parse_scratchpad_info,
    ScratchpadStatus,
    ScratchpadType, parse_scratchpad_target, set_scratchpad_target,
)
from .gateway_result_code import GatewayResultCode


class GetScratchpadStatusRequest(Request):
    """
    GetScratchpadStatusRequest: request to obtain scratchpad status of a given sink

    Attributes:
        sink_id (str): id of the sink (dependant on gateway)
        req_id (int): unique request id
    """

    def __init__(self, sink_id, req_id=None, **kwargs):
        super(GetScratchpadStatusRequest, self).__init__(sink_id, req_id, **kwargs)

    @staticmethod
    def _get_related_message(generic_message):
        return generic_message.wirepas.get_scratchpad_status_req

    @classmethod
    def from_payload(cls, payload):
        req = cls._decode_and_get_related_message(payload)

        d = Request._parse_request_header(req.header)

        return cls(d["sink_id"], d["req_id"], time_ms_epoch=d["time_ms_epoch"])

    @property
    def payload(self):
        message = GenericMessage()
        # Fill the request header
        req = self._get_related_message(message)
        self._load_request_header(req)

        return message.SerializeToString()


class GetScratchpadStatusResponse(Response):
    """
    GetScratchpadStatusResponse: Response to answer a GetScratchpadStatusRequest

    Attributes:
        req_id (int): unique request id that this Response is associated
        gw_id (str): gateway unique identifier
        res (GatewayResultCode): result of the operation
        sink_id (str): id of the sink (dependant on gateway)
        stored_scratchpad(dict): dictionary containing description of stored scratchpad
        stored_status(ScratchpadStatus): status of stored scratchpad
        stored_type(ScratchpadType): type of stored scratchpad
        process_scratchpad(dic): dictionary containing description of processed scratchpad
        target_scratchpad_and_action(dic): dictionary containing target scratchpad and associated action
        firmware_area_id(int): current firmware area id
    """

    def __init__(
        self,
        req_id,
        gw_id,
        res,
        sink_id,
        stored_scratchpad=None,
        stored_status=None,
        stored_type=None,
        processed_scratchpad=None,
        firmware_area_id=None,
        target_scratchpad_and_action=None,
        **kwargs
    ):
        super(GetScratchpadStatusResponse, self).__init__(req_id, gw_id, res, sink_id, **kwargs)
        self.stored_scratchpad = stored_scratchpad
        self.stored_status = stored_status
        self.stored_type = stored_type
        self.processed_scratchpad = processed_scratchpad
        self.firmware_area_id = firmware_area_id
        self.target_scratchpad_and_action = target_scratchpad_and_action

    @staticmethod
    def _get_related_message(generic_message):
        return generic_message.wirepas.get_scratchpad_status_resp

    @classmethod
    def from_payload(cls, payload):
        response = cls._decode_and_get_related_message(payload)

        d = Response._parse_response_header(response.header)

        stored_scratchpad = None
        processed_scratchpad = None
        stored_status = None
        stored_type = None
        firmware_area_id = None
        target_scratchpad_and_action = None

        if response.HasField("stored_scratchpad"):
            stored_scratchpad = dict()
            parse_scratchpad_info(response.stored_scratchpad, stored_scratchpad)

        if response.HasField("processed_scratchpad"):
            processed_scratchpad = dict()
            parse_scratchpad_info(response.processed_scratchpad, processed_scratchpad)

        if response.HasField("stored_status"):
            stored_status = ScratchpadStatus(response.stored_status)

        if response.HasField("stored_type"):
            stored_type = ScratchpadType(response.stored_type)

        if response.HasField("firmware_area_id"):
            firmware_area_id = response.firmware_area_id

        if response.HasField("target_and_action"):
            target_scratchpad_and_action = dict()
            parse_scratchpad_target(response.target_and_action, target_scratchpad_and_action)

        return cls(
            d["req_id"],
            d["gw_id"],
            d["res"],
            d["sink_id"],
            stored_scratchpad,
            stored_status,
            stored_type,
            processed_scratchpad,
            firmware_area_id,
            target_scratchpad_and_action,
            time_ms_epoch=d["time_ms_epoch"]
        )

    @property
    def payload(self):
        message = GenericMessage()

        response = self._get_related_message(message)
        self._load_response_header(response)

        if self.res is not GatewayResultCode.GW_RES_OK:
            # Return code is not OK so do not send message
            return message.SerializeToString()

        if self.stored_scratchpad is not None:
            set_scratchpad_info(response.stored_scratchpad, self.stored_scratchpad)

        if self.processed_scratchpad is not None:
            set_scratchpad_info(
                response.processed_scratchpad, self.processed_scratchpad
            )

        if self.stored_status is not None:
            response.stored_status = self.stored_status.value

        if self.stored_type is not None:
            response.stored_type = self.stored_type.value

        if self.firmware_area_id is not None:
            response.firmware_area_id = self.firmware_area_id

        if self.target_scratchpad_and_action is not None:
            set_scratchpad_target(response.target_and_action, self.target_scratchpad_and_action)

        return message.SerializeToString()
