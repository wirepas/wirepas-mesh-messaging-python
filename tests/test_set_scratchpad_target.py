# flake8: noqa

import enum

import pytest
from default_value import *

import wirepas_mesh_messaging
from wirepas_mesh_messaging.proto.generic_message_pb2 import GenericMessage
from wirepas_mesh_messaging.wirepas_exceptions import InvalidMessageContents


def test_generate_parse_request_with_raw():
    request = wirepas_mesh_messaging.SetScratchpadTargetAndActionRequest(
        SINK_ID, SCRATCHPAD_TARGET_RAW, REQUEST_ID
    )

    request2 = wirepas_mesh_messaging.SetScratchpadTargetAndActionRequest.from_payload(
        request.payload
    )

    for k, v in request.__dict__.items():
        assert v == request2.__dict__[k]


def test_generate_parse_request_with_delay():
    request = wirepas_mesh_messaging.SetScratchpadTargetAndActionRequest(
        SINK_ID, SCRATCHPAD_TARGET_DELAY, REQUEST_ID
    )

    request2 = wirepas_mesh_messaging.SetScratchpadTargetAndActionRequest.from_payload(
        request.payload
    )

    for k, v in request.__dict__.items():
        assert v == request2.__dict__[k]


def test_generate_parse_request_min():
    # Clear a scratchpad
    request = wirepas_mesh_messaging.SetScratchpadTargetAndActionRequest(
        SINK_ID, SCRATCHPAD_TARGET_MIN, REQUEST_ID
    )

    request2 = wirepas_mesh_messaging.SetScratchpadTargetAndActionRequest.from_payload(
        request.payload
    )

    for k, v in request.__dict__.items():
        assert v == request2.__dict__[k]


def test_generate_parse_response():
    request = wirepas_mesh_messaging.SetScratchpadTargetAndActionResponse(
        REQUEST_ID,
        GATEWAY_ID,
        RES_OK,
        SINK_ID
    )

    request2 = wirepas_mesh_messaging.SetScratchpadTargetAndActionResponse.from_payload(
        request.payload
    )

    for k, v in request.__dict__.items():
        if isinstance(v, enum.Enum):
            assert v.value == request2.__dict__[k].value
        else:
            assert v == request2.__dict__[k]


def test_constructing_request_with_too_large_target_sequence_should_fail():
    target_and_action = {
        "action": wirepas_mesh_messaging.ScratchpadAction.ACTION_PROPAGATE_ONLY,
        "target_sequence": 0x100,
    }
    with pytest.raises(ValueError):
        wirepas_mesh_messaging.SetScratchpadTargetAndActionRequest(
            SINK_ID, target_and_action, REQUEST_ID
        )


def test_constructing_request_with_too_large_target_crc_should_fail():
    target_and_action = {
        "action": wirepas_mesh_messaging.ScratchpadAction.ACTION_PROPAGATE_ONLY,
        "target_crc": 0x10000,
    }
    with pytest.raises(ValueError):
        wirepas_mesh_messaging.SetScratchpadTargetAndActionRequest(
            SINK_ID, target_and_action, REQUEST_ID
        )


def test_constructing_request_with_too_large_raw_action_should_fail():
    target_and_action = {
        "action": wirepas_mesh_messaging.ScratchpadAction.ACTION_PROPAGATE_AND_PROCESS,
        "param": 0x100,
    }
    with pytest.raises(ValueError):
        wirepas_mesh_messaging.SetScratchpadTargetAndActionRequest(
            SINK_ID, target_and_action, REQUEST_ID
        )


def test_decoding_request_with_too_large_target_sequence_should_fail_with_correct_exception():
    TEST_TIME = 34567
    base_request = wirepas_mesh_messaging.SetScratchpadTargetAndActionRequest(
        SINK_ID, SCRATCHPAD_TARGET_RAW, REQUEST_ID, time_ms_epoch=TEST_TIME
    )
    message = GenericMessage()
    message.ParseFromString(base_request.payload)
    message.wirepas.set_scratchpad_target_and_action_req.target_and_action.target_sequence = (
        0x100
    )
    test_payload = message.SerializeToString()

    with pytest.raises(InvalidMessageContents) as exc_info:
        wirepas_mesh_messaging.SetScratchpadTargetAndActionRequest.from_payload(
            test_payload
        )
    assert exc_info.value.header["req_id"] == REQUEST_ID
    assert exc_info.value.header["sink_id"] == SINK_ID
    assert exc_info.value.header["time_ms_epoch"] == TEST_TIME


def test_decoding_request_with_too_large_target_crc_should_fail_with_correct_exception():
    TEST_TIME = 1234567
    base_request = wirepas_mesh_messaging.SetScratchpadTargetAndActionRequest(
        SINK_ID_2, SCRATCHPAD_TARGET_RAW, REQUEST_ID, time_ms_epoch=TEST_TIME
    )
    message = GenericMessage()
    message.ParseFromString(base_request.payload)
    message.wirepas.set_scratchpad_target_and_action_req.target_and_action.target_crc = (
        0x10000
    )
    test_payload = message.SerializeToString()

    with pytest.raises(InvalidMessageContents) as exc_info:
        wirepas_mesh_messaging.SetScratchpadTargetAndActionRequest.from_payload(
            test_payload
        )
    assert exc_info.value.header["req_id"] == REQUEST_ID
    assert exc_info.value.header["sink_id"] == SINK_ID_2
    assert exc_info.value.header["time_ms_epoch"] == TEST_TIME
