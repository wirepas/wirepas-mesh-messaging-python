# flake8: noqa

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

    for k, v in status.__dict__.items():
        assert v == status2.__dict__[k]

def test_generate_parse_event_with_max_size():
    status = wirepas_mesh_messaging.StatusEvent(GATEWAY_ID, GATEWAY_STATE, max_scratchpad_size=1024)

    status2 = wirepas_mesh_messaging.StatusEvent.from_payload(status.payload)

    for k, v in status.__dict__.items():
        assert v == status2.__dict__[k]
