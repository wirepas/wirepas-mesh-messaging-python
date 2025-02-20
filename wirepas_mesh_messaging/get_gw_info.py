"""
    Get gateway info
    ================

    .. Copyright:
        Copyright 2019 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""

from .proto import GenericMessage
from .gateway_feature import GatewayFeature

from .request import Request
from .response import Response


class GetGatewayInfoRequest(Request):
    """
    GetGatewayInfoRequest: Request to obtain the gateway config

    Attributes:
        req_id (int): unique request id
    """

    def __init__(self, req_id=None, **kwargs):
        super(GetGatewayInfoRequest, self).__init__(req_id=req_id, **kwargs)

    @staticmethod
    def _get_related_message(generic_message):
        return generic_message.wirepas.get_gateway_info_req

    @classmethod
    def from_payload(cls, payload):
        req = cls._decode_and_get_related_message(payload)

        d = Request._parse_request_header(req.header)
        return cls(d["req_id"], time_ms_epoch=d["time_ms_epoch"])

    @property
    def payload(self):
        message = GenericMessage()
        # Fill the request header
        get_gateway_info = self._get_related_message(message)
        self._load_request_header(get_gateway_info)

        return message.SerializeToString()


class GetGatewayInfoResponse(Response):
    """
    GetGatewayInfoResponse: Response to answer a GetGatewayInfoRequest

    Attributes:
        req_id (int): unique request id that this Response is associated
        gw_id (str): gw_id (str): gateway unique identifier
        res (GatewayResultCode): result of the operation
        current_time_s_epoch (int): current timestamp in ms relative to epoch
        gateway_model (string): gateway model (managed by gateway integrator)
        gateway_version (string): gateway version (managed by gateway integrator)
        max_scratchpad_size (int): max scratchpad size gateway support.
             If bigger, transfer must happen as chunks, if None it is unlimited
        gateway_features (list): list of GatewayFeature objects for supported features
    """

    def __init__(
        self,
        req_id,
        gw_id,
        res,
        current_time_s_epoch,
        gateway_model=None,
        gateway_version=None,
        max_scratchpad_size=None,
        gateway_features=None,
        implemented_api_version=None,
        **kwargs
    ):
        super(GetGatewayInfoResponse, self).__init__(req_id, gw_id, res, **kwargs)
        self.current_time_s_epoch = current_time_s_epoch
        self.gateway_model = gateway_model
        self.gateway_version = gateway_version
        self.implemented_api_version = implemented_api_version
        self.max_scratchpad_size = max_scratchpad_size
        self.gateway_features = gateway_features if gateway_features else []

    @staticmethod
    def _get_related_message(generic_message):
        return generic_message.wirepas.get_gateway_info_resp

    @classmethod
    def from_payload(cls, payload):
        response = cls._decode_and_get_related_message(payload)

        d = Response._parse_response_header(response.header)

        max_size = response.info.max_scratchpad_size
        if max_size == 0:
            max_size = None

        gateway_features = []
        for gateway_feature in response.info.gw_features:
            gateway_features.append(GatewayFeature(gateway_feature))

        return cls(
            d["req_id"],
            d["gw_id"],
            d["res"],
            current_time_s_epoch=response.info.current_time_s_epoch,
            gateway_model=response.info.gw_model,
            gateway_version=response.info.gw_version,
            implemented_api_version=response.info.implemented_api_version,
            max_scratchpad_size=max_size,
            gateway_features=gateway_features,
            time_ms_epoch=d["time_ms_epoch"]
        )

    @property
    def payload(self):
        message = GenericMessage()

        response = self._get_related_message(message)
        self._load_response_header(response)

        response.info.current_time_s_epoch = self.current_time_s_epoch

        if self.gateway_model is not None:
            response.info.gw_model = self.gateway_model

        if self.gateway_version is not None:
            response.info.gw_version = self.gateway_version

        if self.implemented_api_version is not None:
            response.info.implemented_api_version = self.implemented_api_version

        if self.max_scratchpad_size is not None:
            response.info.max_scratchpad_size = self.max_scratchpad_size

        for gateway_feature in self.gateway_features:
            response.info.gw_features.append(gateway_feature.value)

        return message.SerializeToString()
