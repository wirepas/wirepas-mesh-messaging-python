# flake8: noqa

import wirepas_mesh_messaging
from default_value import *
import time

now_ms = int(time.time() * 1000)

def test_automatic_timestamp_request():
    request = wirepas_mesh_messaging.UploadScratchpadRequest(
        SCRATCHPAD_SEQ, SINK_ID, REQUEST_ID
    )

    assert request.time_ms_epoch <= time.time() * 1000

    # Wait a bit explicitly to be sure that if timestamp match,
    # it is because they are reused and regenerated in same ms
    time.sleep(0.1)

    request2 = wirepas_mesh_messaging.UploadScratchpadRequest.from_payload(
        request.payload
    )

    for k, v in request.__dict__.items():
        assert v == request2.__dict__[k]

def test_no_timestamp_request():
    request = wirepas_mesh_messaging.UploadScratchpadRequest(
        SCRATCHPAD_SEQ, SINK_ID, REQUEST_ID, time_ms_epoch=None
    )

    assert request.time_ms_epoch == None

    request2 = wirepas_mesh_messaging.UploadScratchpadRequest.from_payload(
        request.payload
    )

    for k, v in request.__dict__.items():
        assert v == request2.__dict__[k]

def test_timestamp_request():
    request = wirepas_mesh_messaging.UploadScratchpadRequest(
        SCRATCHPAD_SEQ, SINK_ID, REQUEST_ID, time_ms_epoch = now_ms
    )

    assert request.time_ms_epoch == now_ms

    request2 = wirepas_mesh_messaging.UploadScratchpadRequest.from_payload(
        request.payload
    )

    for k, v in request.__dict__.items():
        assert v == request2.__dict__[k]


def test_automatic_timestamp_response():
    response = wirepas_mesh_messaging.UploadScratchpadResponse(
        REQUEST_ID, GATEWAY_ID, RES_OK, SINK_ID
    )

    assert response.time_ms_epoch <= time.time() * 1000

    response2 = wirepas_mesh_messaging.UploadScratchpadResponse.from_payload(
        response.payload
    )

    for k, v in response.__dict__.items():
        assert v == response2.__dict__[k]

def test_no_timestamp_response():
    response = wirepas_mesh_messaging.UploadScratchpadResponse(
        REQUEST_ID, GATEWAY_ID, RES_OK, SINK_ID, time_ms_epoch = None
    )

    assert response.time_ms_epoch == None

    response2 = wirepas_mesh_messaging.UploadScratchpadResponse.from_payload(
        response.payload
    )

    for k, v in response.__dict__.items():
        assert v == response2.__dict__[k]

def test_timestamp_response():
    response = wirepas_mesh_messaging.UploadScratchpadResponse(
        REQUEST_ID, GATEWAY_ID, RES_OK, SINK_ID, time_ms_epoch = now_ms
    )

    assert response.time_ms_epoch == now_ms

    response2 = wirepas_mesh_messaging.UploadScratchpadResponse.from_payload(
        response.payload
    )

    for k, v in response.__dict__.items():
        assert v == response2.__dict__[k]

def test_automatic_timestamp_event():
    status = wirepas_mesh_messaging.StatusEvent(GATEWAY_ID, GATEWAY_STATE)

    assert status.time_ms_epoch <= time.time() * 1000

    status2 = wirepas_mesh_messaging.StatusEvent.from_payload(status.payload)

    for k, v in status.__dict__.items():
        assert v == status2.__dict__[k]

def test_no_timestamp_event():
    status = wirepas_mesh_messaging.StatusEvent(GATEWAY_ID, GATEWAY_STATE, time_ms_epoch = None)

    assert status.time_ms_epoch == None

    status2 = wirepas_mesh_messaging.StatusEvent.from_payload(status.payload)

    for k, v in status.__dict__.items():
        assert v == status2.__dict__[k]

def test__timestamp_event():
    status = wirepas_mesh_messaging.StatusEvent(GATEWAY_ID, GATEWAY_STATE, time_ms_epoch = now_ms)

    assert status.time_ms_epoch == now_ms

    status2 = wirepas_mesh_messaging.StatusEvent.from_payload(status.payload)

    for k, v in status.__dict__.items():
        assert v == status2.__dict__[k]
