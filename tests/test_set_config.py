# flake8: noqa

import pytest
import wirepas_mesh_messaging
from default_value import *
from wirepas_mesh_messaging.wirepas_exceptions import GatewayAPIParsingException


def test_generate_parse_request():
    request = wirepas_mesh_messaging.SetConfigRequest(
        SINK_ID, NODE_CONFIG_1, REQUEST_ID
    )

    request2 = wirepas_mesh_messaging.SetConfigRequest.from_payload(
        request.payload
    )

    for k, v in request.__dict__.items():
        assert v == request2.__dict__[k]


def test_generate_parse_response():
    request = wirepas_mesh_messaging.SetConfigResponse(
        REQUEST_ID, GATEWAY_ID, RES_OK, SINK_ID, NODE_CONFIG_1
    )

    request2 = wirepas_mesh_messaging.SetConfigResponse.from_payload(
        request.payload
    )

    for k, v in request.__dict__.items():
        assert v == request2.__dict__[k]

def test_request_decoding_error():
    with pytest.raises(GatewayAPIParsingException):
        wirepas_mesh_messaging.SetConfigRequest.from_payload(INVALID_PROTOBUF_MESSAGE)

def test_response_decoding_error():
    with pytest.raises(GatewayAPIParsingException):
        wirepas_mesh_messaging.SetConfigResponse.from_payload(INVALID_PROTOBUF_MESSAGE)
