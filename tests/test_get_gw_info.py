# flake8: noqa

import pytest
import wirepas_mesh_messaging
from default_value import *
import time

from wirepas_mesh_messaging.wirepas_exceptions import GatewayAPIParsingException


def test_generate_parse_request():
    request = wirepas_mesh_messaging.GetGatewayInfoRequest(REQUEST_ID)

    request2 = wirepas_mesh_messaging.GetGatewayInfoRequest.from_payload(
        request.payload
    )

    for k, v in request.__dict__.items():
        assert v == request2.__dict__[k]


def test_generate_parse_response():
    request = wirepas_mesh_messaging.GetGatewayInfoResponse(
        REQUEST_ID,
        GATEWAY_ID,
        RES_OK,
        int(time.time()),
        "Gateway model A",
        "Version x.y",
        max_scratchpad_size=512,
        implemented_api_version=IMPLEMENTED_API_VERSION,
    )

    request2 = wirepas_mesh_messaging.GetGatewayInfoResponse.from_payload(
        request.payload
    )

    for k, v in request.__dict__.items():
        assert v == request2.__dict__[k]


def test_generate_parse_response_not_all_optional():
    request = wirepas_mesh_messaging.GetGatewayInfoResponse(
        REQUEST_ID,
        GATEWAY_ID,
        RES_OK,
        int(time.time()),
        "Gateway model A",
        "Version x.y",
        implemented_api_version=IMPLEMENTED_API_VERSION,
    )

    request2 = wirepas_mesh_messaging.GetGatewayInfoResponse.from_payload(
        request.payload
    )

    for k, v in request.__dict__.items():
        print(k)
        assert v == request2.__dict__[k]

def test_request_decoding_error():
    with pytest.raises(GatewayAPIParsingException):
        wirepas_mesh_messaging.GetGatewayInfoRequest.from_payload(INVALID_PROTOBUF_MESSAGE)

def test_response_decoding_error():
    with pytest.raises(GatewayAPIParsingException):
        wirepas_mesh_messaging.GetGatewayInfoResponse.from_payload(INVALID_PROTOBUF_MESSAGE)
