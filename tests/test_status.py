# flake8: noqa

import pytest
import wirepas_mesh_messaging
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

    assert DUMMY_CONFIGS == status2.sink_configs
    for k, v in status.__dict__.items():
        assert v == status2.__dict__[k]

def test_generate_parse_event_with_max_size():
    status = wirepas_mesh_messaging.StatusEvent(GATEWAY_ID, GATEWAY_STATE, max_scratchpad_size=1024)

    status2 = wirepas_mesh_messaging.StatusEvent.from_payload(status.payload)

    for k, v in status.__dict__.items():
        assert v == status2.__dict__[k]

def test_generate_parse_event_with_feature_flags():
    gw_features = [
        wirepas_mesh_messaging.GatewayFeature.GW_FEATURE_SCRATCHPAD_CHUNK_V1,
        wirepas_mesh_messaging.GatewayFeature.GW_FEATURE_CONFIGURATION_DATA_V1
    ]
    status = wirepas_mesh_messaging.StatusEvent(GATEWAY_ID, GATEWAY_STATE, gateway_features=gw_features)

    status_parsed = wirepas_mesh_messaging.StatusEvent.from_payload(status.payload)

    for k, v in status.__dict__.items():
        assert v == status_parsed.__dict__[k]

def test_encoding_message_with_invalid_feature_flag():
    status = wirepas_mesh_messaging.StatusEvent(GATEWAY_ID, GATEWAY_STATE, gateway_features=["INVALID_VALUE12345"])

    with pytest.raises(Exception):
        status.payload

