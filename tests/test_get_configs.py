# flake8: noqa

import wirepas_mesh_messaging
from google.protobuf.json_format import ParseDict
from wirepas_mesh_messaging.proto import GenericMessage
from test_utils import get_cdc_with_base64
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

    for k, v in request.__dict__.items():
        assert v == request2.__dict__[k]

def test_parse_response_with_config_data_items():
    message_description = {
        "wirepas": {
            "get_configs_resp": {
                "header": {"sink_id": "sink0", "req_id": "1", "gw_id": "1", "res": 0},
                "configs": [
                    {
                        "sink_id": "sink0",
                        "configuration_data_content": get_cdc_with_base64(TEST_CDC1)
                    }
                ],
            }
        }
    }

    message = ParseDict(message_description, GenericMessage())
    assert message.IsInitialized()

    response = wirepas_mesh_messaging.GetConfigsResponse.from_payload(
        message.SerializeToString()
    )

    assert response.configs[0]["configuration_data_content"] == TEST_CDC1

