# flake8: noqa

import wirepas_mesh_messaging
from default_value import *


def test_generate_parse_request():
    # Clear a scratchpad
    request = wirepas_mesh_messaging.ProcessScratchpadRequest(
        SINK_ID, REQUEST_ID
    )

    request2 = wirepas_mesh_messaging.ProcessScratchpadRequest.from_payload(
        request.payload
    )

    for k, v in request.__dict__.items():
        assert v == request2.__dict__[k]


def test_generate_parse_response():
    request = wirepas_mesh_messaging.ProcessScratchpadResponse(
        REQUEST_ID, GATEWAY_ID, RES_OK, SINK_ID
    )

    request2 = wirepas_mesh_messaging.ProcessScratchpadResponse.from_payload(
        request.payload
    )

    for k, v in request.__dict__.items():
        assert v == request2.__dict__[k]
