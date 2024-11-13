# flake8: noqa

import pytest
import wirepas_mesh_messaging
import enum
from default_value import *
from wirepas_mesh_messaging.wirepas_exceptions import GatewayAPIParsingException


def test_generate_parse_request_with_raw():
    request = wirepas_mesh_messaging.SetScratchpadTargetAndActionRequest(
        SINK_ID, SCRATCHPAD_TARGET_RAW, REQUEST_ID
    )

    request2 = wirepas_mesh_messaging.SetScratchpadTargetAndActionRequest.from_payload(
        request.payload
    )

    for k, v in request.__dict__.items():
        assert v == request2.__dict__[k]


def test_generate_parse_request_with_delay():
    request = wirepas_mesh_messaging.SetScratchpadTargetAndActionRequest(
        SINK_ID, SCRATCHPAD_TARGET_DELAY, REQUEST_ID
    )

    request2 = wirepas_mesh_messaging.SetScratchpadTargetAndActionRequest.from_payload(
        request.payload
    )

    for k, v in request.__dict__.items():
        assert v == request2.__dict__[k]


def test_generate_parse_request_min():
    # Clear a scratchpad
    request = wirepas_mesh_messaging.SetScratchpadTargetAndActionRequest(
        SINK_ID, SCRATCHPAD_TARGET_MIN, REQUEST_ID
    )

    request2 = wirepas_mesh_messaging.SetScratchpadTargetAndActionRequest.from_payload(
        request.payload
    )

    for k, v in request.__dict__.items():
        assert v == request2.__dict__[k]


def test_generate_parse_response():
    request = wirepas_mesh_messaging.SetScratchpadTargetAndActionResponse(
        REQUEST_ID,
        GATEWAY_ID,
        RES_OK,
        SINK_ID
    )

    request2 = wirepas_mesh_messaging.SetScratchpadTargetAndActionResponse.from_payload(
        request.payload
    )

    for k, v in request.__dict__.items():
        if isinstance(v, enum.Enum):
            assert v.value == request2.__dict__[k].value
        else:
            assert v == request2.__dict__[k]

def test_request_decoding_error():
    with pytest.raises(GatewayAPIParsingException):
        wirepas_mesh_messaging.SetScratchpadTargetAndActionRequest.from_payload(INVALID_PROTOBUF_MESSAGE)

def test_response_decoding_error():
    with pytest.raises(GatewayAPIParsingException):
        wirepas_mesh_messaging.SetScratchpadTargetAndActionResponse.from_payload(INVALID_PROTOBUF_MESSAGE)
