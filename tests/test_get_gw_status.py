# flake8: noqa

import wirepas_mesh_messaging
from default_value import *
import time


def test_generate_parse_request():
    request = wirepas_mesh_messaging.GetGatewayStatusRequest(REQUEST_ID)

    request2 = wirepas_mesh_messaging.GetGatewayStatusRequest.from_payload(
        request.payload
    )

    for k, v in request.__dict__.items():
        assert v == request2.__dict__[k]


def test_generate_parse_response():
    request = wirepas_mesh_messaging.GetGatewayStatusResponse(
        REQUEST_ID,
        GATEWAY_ID,
        RES_OK,
        GATEWAY_STATE,
    )

    request2 = wirepas_mesh_messaging.GetGatewayStatusResponse.from_payload(
        request.payload
    )

    for k, v in request.__dict__.items():
        assert v == request2.__dict__[k]
