"""
    Upload scratchpad
    =================

    .. Copyright:
        Copyright 2019 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""

from .proto import GenericMessage

from .request import Request
from .response import Response


class UploadScratchpadRequest(Request):
    """
    UploadScratchpadRequest: request to process scratchpad on a given sink

    Attributes:
        sink_id (str): id of the sink to upload scratchpad
        req_id (int): unique request id
        scratchpad (bytearray): scratchpad to upload (None to clear scratchpad)
        chunk_info (dic): dictionary containing chunk info
            Dict keys are:
                total_size (int): full size of scratchpad
                offset (int): target crc
    """

    def __init__(self, seq, sink_id, req_id=None, scratchpad=None, chunk_info=None, **kwargs):
        super(UploadScratchpadRequest, self).__init__(sink_id, req_id, **kwargs)
        self.seq = seq
        self.scratchpad = scratchpad
        self.chunk_info = chunk_info

    @staticmethod
    def _get_related_message(generic_message):
        return generic_message.wirepas.upload_scratchpad_req

    @classmethod
    def from_payload(cls, payload):
        req = cls._decode_and_get_related_message(payload)

        d = Request._parse_request_header(req.header)
        if req.HasField("scratchpad"):
            scratchpad = req.scratchpad
        else:
            # Clear the scratchpad
            scratchpad = None

        chunk_info = None
        if req.HasField("chunk_info"):
            chunk_info = {}
            chunk_info["total_size"] = req.chunk_info.scratchpad_total_size
            chunk_info["offset"] = req.chunk_info.start_offset

        return cls(req.seq, d["sink_id"], d["req_id"], scratchpad, time_ms_epoch=d["time_ms_epoch"], chunk_info=chunk_info)

    @property
    def payload(self):
        message = GenericMessage()

        # Fill the request header
        req = self._get_related_message(message)
        self._load_request_header(req)

        req.seq = self.seq
        if self.scratchpad is not None:
            req.scratchpad = self.scratchpad


        if self.chunk_info is not None:
            req.chunk_info.scratchpad_total_size = self.chunk_info["total_size"]
            req.chunk_info.start_offset = self.chunk_info["offset"]

        return message.SerializeToString()


class UploadScratchpadResponse(Response):
    """
    UploadScratchpadResponse: Response to answer a UploadScratchpadRequest

    Attributes:
        req_id (int): unique request id that this Response is associated
        gw_id (str): gw_id (str): gateway unique identifier
        res (GatewayResultCode): result of the operation
        sink_id (str): id of the sink (dependant on gateway)
    """

    def __init__(self, req_id, gw_id, res, sink_id, **kwargs):
        super(UploadScratchpadResponse, self).__init__(
            req_id, gw_id, res, sink_id, **kwargs
        )

    @staticmethod
    def _get_related_message(generic_message):
        return generic_message.wirepas.upload_scratchpad_resp

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
