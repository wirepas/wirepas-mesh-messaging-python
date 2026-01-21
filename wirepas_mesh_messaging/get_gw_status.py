"""
    Get gateway status
    ================

    .. Copyright:
        Copyright 2019 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""

from .proto import GenericMessage, ON, OFF

from .request import Request
from .response import Response
from .status import GatewayState, API_VERSION

from .wirepas_exceptions import GatewayAPIParsingException


class GetGatewayStatusRequest(Request):
    """
    GetGatewayStatusRequest: Request to obtain the gateway status

    Attributes:
        req_id (int): unique request id
    """

    def __init__(self, req_id=None, **kwargs):
        super(GetGatewayStatusRequest, self).__init__(req_id=req_id, **kwargs)

    @classmethod
    def from_payload(cls, payload):
        message = GenericMessage()
        try:
            message.ParseFromString(payload)
        except Exception:
            # Any Exception is promoted to Generic API exception
            raise GatewayAPIParsingException(
                "Cannot parse GetGatewayStatusRequest payload"
            )

        d = Request._parse_request_header(message.wirepas.get_gateway_status_req.header)
        return cls(d["req_id"])

    @property
    def payload(self):
        message = GenericMessage()
        # Fill the request header
        get_gateway_status = message.wirepas.get_gateway_status_req
        self._load_request_header(get_gateway_status)

        return message.SerializeToString()


class GetGatewayStatusResponse(Response):
    """
    GetGatewayStatusResponse: Response to answer a GetGatewayStatusRequest

    Attributes:
        req_id (int): unique request id that this Response is associated
        gw_id (str): gw_id (str): gateway unique identifier
        res (GatewayResultCode): result of the operation
        state (GatewayState): state of the gateway
        version (int): API version for gateway. Should be always 1
    """

    def __init__(
        self,
        req_id,
        gw_id,
        res,
        state,
        version=API_VERSION,
        **kwargs
    ):
        super(GetGatewayStatusResponse, self).__init__(req_id, gw_id, res, **kwargs)
        self.version = version
        self.state = state

    @classmethod
    def from_payload(cls, payload):
        message = GenericMessage()
        try:
            message.ParseFromString(payload)
        except Exception:
            # Any Exception is promoted to Generic API exception
            raise GatewayAPIParsingException(
                "Cannot parse GetGatewayStatusResponse payload"
            )

        response = message.wirepas.get_gateway_status_resp

        if response.status.state == ON:
            online = GatewayState.ONLINE
        else:
            online = GatewayState.OFFLINE

        if response.status.version != API_VERSION:
            raise RuntimeError("Wrong API version")

        d = Response._parse_response_header(response.header)

        return cls(
            d["req_id"],
            d["gw_id"],
            d["res"],
            online,
        )

    @property
    def payload(self):
        message = GenericMessage()

        response = message.wirepas.get_gateway_status_resp
        self._load_response_header(response)

        response.status.version = API_VERSION
        if self.state == GatewayState.ONLINE:
            response.status.state = ON
        else:
            response.status.state = OFF

        return message.SerializeToString()
