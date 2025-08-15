# flake8: noqa

import wirepas_mesh_messaging

# Define list of default values used during testing
GATEWAY_ID = "test_gateway"
GATEWAY_STATE = wirepas_mesh_messaging.GatewayState.ONLINE
SINK_ID = "sink3"
SINK_ID_2 = "sink7"
RES_OK = wirepas_mesh_messaging.GatewayResultCode.GW_RES_OK
RES_KO = wirepas_mesh_messaging.GatewayResultCode.GW_RES_INTERNAL_ERROR
REQUEST_ID = 1234567
DESTINATION_ADD = 5678
SOURCE_ADD = 1234
SOURCE_EP = 98
DESTINATION_EP = 127
QOS = 0
DATA_PAYLOAD = bytes(b"Test")
INITIAL_DELAY = 12
RX_TIME_MS_EPOCH = int(123456789)
TRAVEL_TIME_MS = 123
HOP_COUNT = 10
NETWORK_ADDRESS = 0x123456

IMPLEMENTED_API_VERSION = 0

TEST_CDC1 = [
    { "endpoint": 1,       "payload": bytes.fromhex("AABBCCDDEEFF") },
    { "endpoint": 0x20000, "payload": bytes.fromhex("334455") },
]

# Todo add more fields in config
NODE_CONFIG_1 = dict([("sink_id", SINK_ID), ("node_address", 123)])


SCRATCHPAD_SEQ = 12
SCRATCHPAD = bytes(bytearray(1024))

SCRATCHPAD_INFO = dict([("len", 2032), ("crc", 0x1234), ("seq", 112)])

SCRATCHPAD_TARGET_RAW = dict([("action", wirepas_mesh_messaging.ScratchpadAction.ACTION_PROPAGATE_AND_PROCESS),
                          ("target_sequence", 18),
                          ("param", 123)])

SCRATCHPAD_TARGET_DELAY = dict([("action", wirepas_mesh_messaging.ScratchpadAction.ACTION_PROPAGATE_AND_PROCESS_WITH_DELAY),
                          ("target_sequence", 18),
                          ("delay", wirepas_mesh_messaging.ProcessingDelay.DELAY_FIVE_DAYS)])

SCRATCHPAD_TARGET_MIN = dict([("action", wirepas_mesh_messaging.ScratchpadAction.ACTION_PROPAGATE_ONLY)])

SCRATCHPAD_STATUS = wirepas_mesh_messaging.ScratchpadStatus.SCRATCHPAD_STATUS_SUCCESS
SCRATCHPAD_TYPE = wirepas_mesh_messaging.ScratchpadType.SCRATCHPAD_TYPE_PRESENT
FIRMWARE_AREA_ID = 0x123456

NODE_CONFIG_2 = dict(
    [("sink_id", SINK_ID_2),
     ("node_address", 456),
     ("target_and_action", SCRATCHPAD_TARGET_DELAY),
     ("firmware_area_id", FIRMWARE_AREA_ID),
     ("stored_type", SCRATCHPAD_TYPE),
     ("stored_status", SCRATCHPAD_STATUS),
     ("processed_scratchpad", SCRATCHPAD_INFO),
     ("stored_scratchpad", SCRATCHPAD_INFO),
     ("configuration_data_content", TEST_CDC1)
    ])

NODE_CONFIG_FOR_SETTING = {
    "sink_id": SINK_ID,
    "node_role": 1,
    "node_address": 1516,
    "network_address": 879123,
    "network_channel": 7,
    "app_config_diag": 30,
    "app_config_seq": 300,
    "app_config_data": bytes.fromhex("90807060"),
    "channel_map": 120,
    "cipher_key": bytes.fromhex("102030"),
    "authentication_key": bytes.fromhex("AABBCC"),
    "started": True,
    "network_keys": {
        "cipher": bytes.fromhex("5000"),
        "authentication": bytes.fromhex("6000"),
        "sequence": 6767
    },
    "management_keys": {
        "cipher": bytes.fromhex("10AA"),
        "authentication": bytes.fromhex("20BB"),
        "sequence": 520
    },
}

