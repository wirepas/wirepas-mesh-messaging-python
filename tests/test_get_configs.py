# flake8: noqa

import wirepas_mesh_messaging
from default_value import *

DUMMY_CONFIGS = [NODE_CONFIG_2]


def test_generate_parse_request():
    request = wirepas_mesh_messaging.GetConfigsRequest(REQUEST_ID)

    request2 = wirepas_mesh_messaging.GetConfigsRequest.from_payload(
        request.payload
    )

    for k, v in request.__dict__.items():
        assert v == request2.__dict__[k]


def test_generate_parse_response():
    request = wirepas_mesh_messaging.GetConfigsResponse(
        REQUEST_ID, GATEWAY_ID, RES_OK, DUMMY_CONFIGS
    )

    request2 = wirepas_mesh_messaging.GetConfigsResponse.from_payload(
        request.payload
    )

    assert DUMMY_CONFIGS == request2.configs
    for k, v in request.__dict__.items():
        assert v == request2.__dict__[k]

