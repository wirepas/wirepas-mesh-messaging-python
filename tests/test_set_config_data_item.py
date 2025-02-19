# flake8: noqa

import pytest
import base64
import wirepas_mesh_messaging
from wirepas_mesh_messaging.proto import GenericMessage
from google.protobuf.json_format import ParseDict
from default_value import *


def test_parse_request_message():
    TEST_REQ_ID = 300
    TEST_ENDPOINT = 500
    TEST_PAYLOAD = bytes.fromhex("AABBCCDDEEFF")

    message_description = {
        "wirepas": {
            "set_configuration_data_item_req": {
                "header": {"req_id": TEST_REQ_ID},
                "configuration_data_item": {
                    "endpoint": TEST_ENDPOINT,
                    # bytes objects are base64 encoded in protobuf JSON format
                    "payload": base64.b64encode(TEST_PAYLOAD)
                }
            }
        }
    }

    message = ParseDict(message_description, GenericMessage())
    assert message.IsInitialized()

    request = wirepas_mesh_messaging.SetConfigurationDataItemRequest.from_payload(
        message.SerializeToString()
    )

    assert TEST_REQ_ID == request.req_id
    assert TEST_ENDPOINT == request.cdc_endpoint
    assert TEST_PAYLOAD == request.cdc_payload

def test_encode_request_message():
    TEST_ENDPOINT = 1000
    TEST_PAYLOAD = bytes.fromhex("102030")

    request = wirepas_mesh_messaging.SetConfigurationDataItemRequest(SINK_ID, TEST_ENDPOINT, TEST_PAYLOAD)

    parsed_request = wirepas_mesh_messaging.SetConfigurationDataItemRequest.from_payload(request.payload)

    for k, v in request.__dict__.items():
        assert v == parsed_request.__dict__[k]

def test_encode_request_with_empty_payload():
    request = wirepas_mesh_messaging.SetConfigurationDataItemRequest(SINK_ID, 100, bytes())
    parsed_request = wirepas_mesh_messaging.SetConfigurationDataItemRequest.from_payload(request.payload)

    assert bytes() == parsed_request.cdc_payload

def test_encoding_request_with_none_payload_should_fail():
    request = wirepas_mesh_messaging.SetConfigurationDataItemRequest(SINK_ID, 100, None)

    with pytest.raises(TypeError):
        request.payload

def test_parse_response_message():
    message_description = {
        "wirepas": {
            "set_configuration_data_item_resp": {
                "header": {
                    "req_id": REQUEST_ID,
                    "gw_id": GATEWAY_ID,
                    "sink_id": SINK_ID_2,
                    "res": 0,
                    "time_ms_epoch": RX_TIME_MS_EPOCH
                }
            }
        }
    }

    message = ParseDict(message_description, GenericMessage())
    assert message.IsInitialized()

    response = wirepas_mesh_messaging.SetConfigurationDataItemResponse.from_payload(
        message.SerializeToString()
    )

    assert REQUEST_ID == response.req_id
    assert GATEWAY_ID == response.gw_id
    assert SINK_ID_2 == response.sink_id
    assert RES_OK == response.res
    assert RX_TIME_MS_EPOCH == response.time_ms_epoch

def test_encode_response_message():
    request = wirepas_mesh_messaging.SetConfigurationDataItemResponse(REQUEST_ID, GATEWAY_ID, RES_OK, SINK_ID)

    parsed_request = wirepas_mesh_messaging.SetConfigurationDataItemResponse.from_payload(request.payload)

    for k, v in request.__dict__.items():
        assert v == parsed_request.__dict__[k]

