# flake8: noqa

import wirepas_mesh_messaging
import enum
from default_value import *


def test_generate_parse_request():
    # Clear a scratchpad
    request = wirepas_mesh_messaging.GetScratchpadStatusRequest(
        SINK_ID, REQUEST_ID
    )

    request2 = wirepas_mesh_messaging.GetScratchpadStatusRequest.from_payload(
        request.payload
    )

    for k, v in request.__dict__.items():
        assert v == request2.__dict__[k]


def test_generate_parse_response():
    request = wirepas_mesh_messaging.GetScratchpadStatusResponse(
        REQUEST_ID,
        GATEWAY_ID,
        RES_OK,
        SINK_ID,
        SCRATCHPAD_INFO,
        SCRATCHPAD_STATUS,
        SCRATCHPAD_TYPE,
        SCRATCHPAD_INFO,
        FIRMWARE_AREA_ID,
        SCRATCHPAD_TARGET_DELAY,
    )

    request2 = wirepas_mesh_messaging.GetScratchpadStatusResponse.from_payload(
        request.payload
    )

    for k, v in request.__dict__.items():
        if isinstance(v, enum.Enum):
            assert v.value == request2.__dict__[k].value
        else:
            assert v == request2.__dict__[k]
