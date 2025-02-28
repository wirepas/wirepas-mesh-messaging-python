# flake8: noqa

import pytest
import base64
import wirepas_mesh_messaging
from wirepas_mesh_messaging.proto import GenericMessage
from google.protobuf.json_format import ParseDict
from default_value import *


def test_parse_request_message():
    TEST_REQ_ID = 200
    TEST_ENDPOINT = 3000

    message_description = {
        "wirepas": {
            "get_configuration_data_item_req": {
                "header": {"req_id": TEST_REQ_ID},
                "endpoint": TEST_ENDPOINT
            }
        }
    }

    message = ParseDict(message_description, GenericMessage())
    assert message.IsInitialized()

    request = wirepas_mesh_messaging.GetConfigurationDataItemRequest.from_payload(
        message.SerializeToString()
    )

    assert TEST_REQ_ID == request.req_id
    assert TEST_ENDPOINT == request.cdc_endpoint

def test_encode_request_message():
    TEST_ENDPOINT = 2000

    request = wirepas_mesh_messaging.GetConfigurationDataItemRequest(SINK_ID, TEST_ENDPOINT)

    parsed_request = wirepas_mesh_messaging.GetConfigurationDataItemRequest.from_payload(request.payload)

    for k, v in request.__dict__.items():
        assert v == parsed_request.__dict__[k]

def test_parse_response_message():
    TEST_ENDPOINT = 700
    TEST_PAYLOAD = bytes.fromhex("BBAABBAADDAADDAA")

    message_description = {
        "wirepas": {
            "get_configuration_data_item_resp": {
                "header": {
                    "req_id": REQUEST_ID,
                    "gw_id": GATEWAY_ID,
                    "sink_id": SINK_ID_2,
                    "res": 0,
                    "time_ms_epoch": RX_TIME_MS_EPOCH
                },
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

    response = wirepas_mesh_messaging.GetConfigurationDataItemResponse.from_payload(
        message.SerializeToString()
    )

    assert REQUEST_ID == response.req_id
    assert GATEWAY_ID == response.gw_id
    assert SINK_ID_2 == response.sink_id
    assert RES_OK == response.res
    assert RX_TIME_MS_EPOCH == response.time_ms_epoch
    assert TEST_ENDPOINT == response.cdc_endpoint
    assert TEST_PAYLOAD == response.cdc_payload

def test_encode_response_message():
    TEST_ENDPOINT = 9000
    TEST_PAYLOAD = bytes.fromhex("FEFE1234")

    request = wirepas_mesh_messaging.GetConfigurationDataItemResponse(
        REQUEST_ID, GATEWAY_ID, RES_OK, SINK_ID, TEST_ENDPOINT, TEST_PAYLOAD
    )

    parsed_request = wirepas_mesh_messaging.GetConfigurationDataItemResponse.from_payload(request.payload)

    for k, v in request.__dict__.items():
        assert v == parsed_request.__dict__[k]

def test_encode_response_with_no_item():
    response = wirepas_mesh_messaging.GetConfigurationDataItemResponse(
        REQUEST_ID, GATEWAY_ID, RES_KO, SINK_ID
    )
    parsed_response = wirepas_mesh_messaging.GetConfigurationDataItemResponse.from_payload(response.payload)

    assert None == parsed_response.cdc_endpoint
    assert None == parsed_response.cdc_payload

def test_encode_response_with_empty_payload():
    TEST_ENDPOINT = 543
    TEST_PAYLOAD = bytes()
    response = wirepas_mesh_messaging.GetConfigurationDataItemResponse(
        REQUEST_ID, GATEWAY_ID, RES_KO, SINK_ID, TEST_ENDPOINT, TEST_PAYLOAD
    )
    parsed_response = wirepas_mesh_messaging.GetConfigurationDataItemResponse.from_payload(response.payload)

    assert TEST_ENDPOINT == parsed_response.cdc_endpoint
    assert TEST_PAYLOAD == parsed_response.cdc_payload

def test_encoding_response_with_endpoint_but_no_payload_should_fail():
    response = wirepas_mesh_messaging.GetConfigurationDataItemResponse(
        REQUEST_ID, GATEWAY_ID, RES_KO, SINK_ID, 1000
    )

    with pytest.raises(Exception):
        response.payload

