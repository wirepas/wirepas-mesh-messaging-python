# flake8: noqa

import wirepas_mesh_messaging
from default_value import *


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


def test_generate_parse_response_with_readonly_fields():
    request = wirepas_mesh_messaging.SetConfigResponse(
        REQUEST_ID, GATEWAY_ID, RES_OK, SINK_ID_2, NODE_CONFIG_2
    )

    request2 = wirepas_mesh_messaging.SetConfigResponse.from_payload(
        request.payload
    )

    assert NODE_CONFIG_2 == request2.config
    for k, v in request.__dict__.items():
        assert v == request2.__dict__[k]


def test_generate_parse_request_with_writeable_fields():
    request = wirepas_mesh_messaging.SetConfigRequest(
        SINK_ID, NODE_CONFIG_FOR_SETTING, REQUEST_ID
    )

    request2 = wirepas_mesh_messaging.SetConfigRequest.from_payload(
        request.payload
    )

    assert NODE_CONFIG_FOR_SETTING == request2.new_config
    for k, v in request.__dict__.items():
        assert v == request2.__dict__[k]

