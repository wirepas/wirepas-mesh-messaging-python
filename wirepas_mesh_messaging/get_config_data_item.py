"""
    Set configuration data item
    ==========

    .. Copyright:
        Copyright 2025 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""

from .proto import GenericMessage

from .request import Request
from .response import Response


class GetConfigurationDataItemRequest(Request):
    """
    GetConfigurationDataItemRequest: request to get a configuration data item
                                     on a given sink

    Attributes:
        sink_id (str): id of the sink (dependant on gateway)
        cdc_endpoint (int): configuration data item endpoint
        req_id (int): unique request id

    """
    def __init__(self, sink_id, cdc_endpoint, req_id=None, **kwargs):
        super().__init__(req_id=req_id, **kwargs)
        self.sink_id = sink_id
        self.cdc_endpoint = cdc_endpoint

    @staticmethod
    def _get_related_message(generic_message):
        return generic_message.wirepas.get_configuration_data_item_req

    @classmethod
    def from_payload(cls, payload):
        req = cls._decode_and_get_related_message(payload)

        header = Request._parse_request_header(req.header)

        return cls(req.header.sink_id,
                   req.endpoint,
                   req_id=header["req_id"],
                   time_ms_epoch=header["time_ms_epoch"])

    @property
    def payload(self):
        message = GenericMessage()

        req_msg = self._get_related_message(message)
        self._load_request_header(req_msg)

        req_msg.endpoint = self.cdc_endpoint

        return message.SerializeToString()


class GetConfigurationDataItemResponse(Response):
    """
    GetConfigurationDataItemResponse: Response to answer a GetConfigurationDataItemRequest

    Attributes:
        req_id (int): unique request id that this Response is associated
        gw_id (str): gateway unique identifier
        res (GatewayResultCode): result of the operation
        sink_id (str): id of the sink (dependant on gateway)
        cdc_endpoint (int): configuration data item endpoint. Optional.
                            If provided, cdc_payload should be provided too.
        cdc_payload (bytes): configuration data item payload. Optional.
                             If provided, cdc_endpoint should be provided too.
    """
    def __init__(self, req_id, gw_id, res, sink_id, cdc_endpoint=None, cdc_payload=None, **kwargs):
        super().__init__(req_id, gw_id, res, sink_id, **kwargs)
        self.cdc_endpoint = cdc_endpoint
        self.cdc_payload = cdc_payload

    @staticmethod
    def _get_related_message(generic_message):
        return generic_message.wirepas.get_configuration_data_item_resp

    @classmethod
    def from_payload(cls, payload):
        response = cls._decode_and_get_related_message(payload)

        header = Response._parse_response_header(response.header)

        cdc_endpoint = None
        cdc_payload = None
        if response.configuration_data_item.IsInitialized():
            cdc_endpoint = response.configuration_data_item.endpoint
            cdc_payload = response.configuration_data_item.payload

        return cls(header["req_id"],
                   header["gw_id"],
                   header["res"],
                   header["sink_id"],
                   cdc_endpoint,
                   cdc_payload,
                   time_ms_epoch=header["time_ms_epoch"])

    @property
    def payload(self):
        message = GenericMessage()

        response = self._get_related_message(message)
        self._load_response_header(response)

        if self.cdc_endpoint is not None:
            response.configuration_data_item.endpoint = self.cdc_endpoint
        if self.cdc_payload is not None:
            response.configuration_data_item.payload = self.cdc_payload

        return message.SerializeToString()
