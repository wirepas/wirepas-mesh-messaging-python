# flake8: noqa

import wirepas_mesh_messaging
from google.protobuf.json_format import ParseDict
from wirepas_mesh_messaging.proto import GenericMessage
from wirepas_mesh_messaging.proto import StatusEvent as StatusEvent_pb
from test_utils import get_cdc_with_base64
from default_value import *

DUMMY_CONFIGS = [NODE_CONFIG_1, NODE_CONFIG_2]

def test_generate_parse_event():
    status = wirepas_mesh_messaging.StatusEvent(GATEWAY_ID, GATEWAY_STATE)

    status2 = wirepas_mesh_messaging.StatusEvent.from_payload(status.payload)

    for k, v in status.__dict__.items():
        assert v == status2.__dict__[k]

def test_generate_parse_event_complete():
    status = wirepas_mesh_messaging.StatusEvent(GATEWAY_ID, GATEWAY_STATE, sink_configs=DUMMY_CONFIGS, gateway_model="test123", gateway_version="v0.1")

    status2 = wirepas_mesh_messaging.StatusEvent.from_payload(status.payload)

    for k, v in status.__dict__.items():
        assert v == status2.__dict__[k]

def test_generate_parse_event_with_max_size():
    status = wirepas_mesh_messaging.StatusEvent(GATEWAY_ID, GATEWAY_STATE, max_scratchpad_size=1024)

    status2 = wirepas_mesh_messaging.StatusEvent.from_payload(status.payload)

    for k, v in status.__dict__.items():
        assert v == status2.__dict__[k]

def test_generate_parse_event_with_feature_flags():
    gw_features = [
        wirepas_mesh_messaging.OptionalGatewayFeature.OTAP_AS_CHUNK,
        wirepas_mesh_messaging.OptionalGatewayFeature.CDD_API
    ]
    status = wirepas_mesh_messaging.StatusEvent(GATEWAY_ID, GATEWAY_STATE, gw_features=gw_features)

    status2 = wirepas_mesh_messaging.StatusEvent.from_payload(status.payload)

    for k, v in status.__dict__.items():
        assert v == status2.__dict__[k]

def test_parse_with_config_data_items():
    message_description = {
        "wirepas": {
            "status_event": {
                "header": {"gw_id": "1", "event_id": 1},
                "version": 1,
                "state": 1,
                "configs": [
                    {
                        "sink_id": "sink0",
                        "configuration_data_content": get_cdc_with_base64(TEST_CDC1)
                    }
                ]
            }
        }
    }
    message = ParseDict(message_description, GenericMessage())
    assert message.IsInitialized()

    status = wirepas_mesh_messaging.StatusEvent.from_payload(
        message.SerializeToString()
    )

    assert status.sink_configs[0]["configuration_data_content"] == TEST_CDC1

def test_parse_with_feature_flags():
    message_description = {
        "wirepas": {
            "status_event": {
                "header": {"gw_id": "1", "event_id": 1},
                "version": 1,
                "state": 1,
                "gw_features": [
                    "CDD_API"
                ]
            }
        }
    }
    message = ParseDict(message_description, GenericMessage())
    assert message.IsInitialized()

    status = wirepas_mesh_messaging.StatusEvent.from_payload(
        message.SerializeToString()
    )

    assert status.gw_features == [ wirepas_mesh_messaging.OptionalGatewayFeature.CDD_API ]

def test_feature_flags():
    """
    Make sure all the feature flags in the internal
    (wirepas_mesh_messaging.OptionalGatewayFeature) enum are aligned with the
    protobuf side if the protobuf definition is updated in this library.
    """

    all_flags_internal = list(wirepas_mesh_messaging.OptionalGatewayFeature)
    all_flags_proto = StatusEvent_pb.OptionalGatewayFeature.values()

    proto_to_internal = []
    for flag in all_flags_proto:
        converted = wirepas_mesh_messaging.OptionalGatewayFeature(flag)
        proto_to_internal.append(converted)

    assert all_flags_internal == proto_to_internal

