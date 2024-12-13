# flake8: noqa

import wirepas_mesh_messaging
import pytest
from google.protobuf.json_format import ParseDict
from wirepas_mesh_messaging.proto import GenericMessage
from test_utils import get_cdc_with_base64
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

def test_parse_request_with_config_data_items():
    message_description = {
        "wirepas": {
            "set_config_req": {
                "header": {"req_id": "1"},
                "config": {
                    "sink_id": "sink0",
                    "configuration_data_content": get_cdc_with_base64(TEST_CDC1)
                },
            }
        }
    }
    message = ParseDict(message_description, GenericMessage())
    assert message.IsInitialized()

    request = wirepas_mesh_messaging.SetConfigRequest.from_payload(
        message.SerializeToString()
    )

    assert request.new_config["configuration_data_content"] == TEST_CDC1

def test_parse_response_with_config_data_items():
    message_description = {
        "wirepas": {
            "set_config_resp": {
                "header": {"sink_id": "sink0", "req_id": "1", "gw_id": "1", "res": 0},
                "config": {
                    "sink_id": "sink0",
                    "configuration_data_content": get_cdc_with_base64(TEST_CDC1)
                },
            }
        }
    }
    message = ParseDict(message_description, GenericMessage())
    assert message.IsInitialized()

    response = wirepas_mesh_messaging.SetConfigResponse.from_payload(
        message.SerializeToString()
    )

    assert response.config["configuration_data_content"] == TEST_CDC1

INVALID_CDC_DATA = [
    ([{ "payload": bytes.fromhex("10") }], KeyError),
    ([{ "endpoint": 10 }], KeyError),
    ({"endpoint": 10, "payload": bytes()}, TypeError),
    ([{"endpoint": -1, "payload": bytes([1,2,3])}], ValueError)
]
@pytest.mark.parametrize("cdc,expected_error", INVALID_CDC_DATA)
def test_request_with_invalid_configuration_data_content(cdc, expected_error):
    TEST_CONFIG = { "configuration_data_content": cdc }
    request = wirepas_mesh_messaging.SetConfigRequest(
        SINK_ID, TEST_CONFIG, REQUEST_ID
    )

    with pytest.raises(expected_error):
        request.payload

@pytest.mark.parametrize("cdc,expected_error", INVALID_CDC_DATA)
def test_response_with_invalid_configuration_data_content(cdc, expected_error):
    TEST_CONFIG = { "configuration_data_content": cdc }
    response = wirepas_mesh_messaging.SetConfigResponse(
        REQUEST_ID, GATEWAY_ID, RES_OK, SINK_ID, TEST_CONFIG
    )

    with pytest.raises(expected_error):
        response.payload

