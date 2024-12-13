# flake8: noqa

import wirepas_mesh_messaging
import pytest
import base64
from google.protobuf.json_format import ParseDict
from wirepas_mesh_messaging.proto import GenericMessage
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
    message_description = _get_request_base()
    config = message_description["wirepas"]["set_config_req"]["config"]
    config["configuration_data_content"] = [
        { "endpoint": 10,      "payload": _hex_to_base64("AABBCC") },
        { "endpoint": 0x10000, "payload": _hex_to_base64("112233EEFF") },
        { "endpoint": 0,       "payload": _hex_to_base64("") }
    ]
    message = ParseDict(message_description, GenericMessage())
    assert message.IsInitialized()

    request = wirepas_mesh_messaging.SetConfigRequest.from_payload(
        message.SerializeToString()
    )

    parsed_cdc = request.new_config["configuration_data_content"]
    assert len(parsed_cdc) == 3
    for expected, parsed in zip(config["configuration_data_content"], parsed_cdc):
        assert parsed["endpoint"] == expected["endpoint"]
        assert parsed["payload"] == base64.b64decode(expected["payload"])

def test_parse_response_with_config_data_items():
    message_description = _get_response_base()
    config = message_description["wirepas"]["set_config_resp"]["config"]
    config["configuration_data_content"] = [
        { "endpoint": 30,      "payload": _hex_to_base64("CCBBAA") },
        { "endpoint": 0x30000, "payload": _hex_to_base64("1122334455") },
        { "endpoint": 0,       "payload": _hex_to_base64("") }
    ]
    message = ParseDict(message_description, GenericMessage())
    assert message.IsInitialized()

    response = wirepas_mesh_messaging.SetConfigResponse.from_payload(
        message.SerializeToString()
    )

    parsed_cdc = response.config["configuration_data_content"]
    assert len(parsed_cdc) == 3
    for expected, parsed in zip(config["configuration_data_content"], parsed_cdc):
        assert parsed["endpoint"] == expected["endpoint"]
        assert parsed["payload"] == base64.b64decode(expected["payload"])

def test_create_request_with_config_data_items():
    TEST_CONFIG = {
        "sink_id": SINK_ID,
        "configuration_data_content": [
            { "endpoint": 5,       "payload": bytes.fromhex("1020304050") },
            { "endpoint": 0x20000, "payload": bytes.fromhex("334455") },
            { "endpoint": 30, "payload": bytes() }
        ]
    }
    built_request = wirepas_mesh_messaging.SetConfigRequest(
        SINK_ID, TEST_CONFIG, REQUEST_ID
    )
    parsed_request = wirepas_mesh_messaging.SetConfigRequest.from_payload(
        built_request.payload
    )

    for k, v in built_request.__dict__.items():
        assert v == parsed_request.__dict__[k]

def test_create_response_with_config_data_items():
    TEST_CONFIG = {
        "sink_id": SINK_ID,
        "configuration_data_content": [
            { "endpoint": 5,       "payload": bytes.fromhex("1020304050") },
            { "endpoint": 0x20000, "payload": bytes.fromhex("334455") },
            { "endpoint": 30, "payload": bytes() }
        ]
    }
    built_response = wirepas_mesh_messaging.SetConfigResponse(
        REQUEST_ID, GATEWAY_ID, RES_OK, SINK_ID, TEST_CONFIG
    )
    parsed_response = wirepas_mesh_messaging.SetConfigResponse.from_payload(
        built_response.payload
    )

    for k, v in built_response.__dict__.items():
        assert v == parsed_response.__dict__[k]

INVALID_CDC_DATA = [
    ([{ "payload": bytes.fromhex("10") }], KeyError),
    ([{ "endpoint": 10 }], KeyError),
    ({"endpoint": 10, "payload": bytes()}, TypeError)
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

def _hex_to_base64(hex_str):
    return base64.b64encode(bytes.fromhex(hex_str))

def _get_request_base() -> dict:
    return {
        "wirepas": {
            "set_config_req": {
                "header": {"req_id": "1"},
                "config": {"sink_id": "sink0"},
            }
        }
    }

def _get_response_base() -> dict:
    return {
        "wirepas": {
            "set_config_resp": {
                "header": {"sink_id": "sink0", "req_id": "1", "gw_id": "1", "res": 0},
                "config": {"sink_id": "sink0"},
            }
        }
    }
