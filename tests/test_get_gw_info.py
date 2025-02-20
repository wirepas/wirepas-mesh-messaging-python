# flake8: noqa

import wirepas_mesh_messaging
from default_value import *
import time


def test_generate_parse_request():
    request = wirepas_mesh_messaging.GetGatewayInfoRequest(REQUEST_ID)

    request2 = wirepas_mesh_messaging.GetGatewayInfoRequest.from_payload(
        request.payload
    )

    for k, v in request.__dict__.items():
        assert v == request2.__dict__[k]


def test_generate_parse_response():
    request = wirepas_mesh_messaging.GetGatewayInfoResponse(
        REQUEST_ID,
        GATEWAY_ID,
        RES_OK,
        int(time.time()),
        "Gateway model A",
        "Version x.y",
        max_scratchpad_size=512,
        implemented_api_version=IMPLEMENTED_API_VERSION,
        gateway_features=[
            wirepas_mesh_messaging.GatewayFeature.GW_FEATURE_SCRATCHPAD_CHUNK_V1,
            wirepas_mesh_messaging.GatewayFeature.GW_FEATURE_CONFIGURATION_DATA_V1
        ]
    )

    request2 = wirepas_mesh_messaging.GetGatewayInfoResponse.from_payload(
        request.payload
    )

    expected_members = [
        "gw_id",
        "sink_id",
        "req_id",
        "res",
        "time_ms_epoch",
        "current_time_s_epoch",
        "gateway_model",
        "gateway_version",
        "implemented_api_version",
        "max_scratchpad_size",
        "gateway_features"
    ]
    for field in expected_members:
        assert field in request.__dict__
        assert field in request2.__dict__

    for k, v in request.__dict__.items():
        assert v == request2.__dict__[k]


def test_generate_parse_response_not_all_optional():
    request = wirepas_mesh_messaging.GetGatewayInfoResponse(
        REQUEST_ID,
        GATEWAY_ID,
        RES_OK,
        int(time.time()),
        "Gateway model A",
        "Version x.y",
        implemented_api_version=IMPLEMENTED_API_VERSION,
    )

    request2 = wirepas_mesh_messaging.GetGatewayInfoResponse.from_payload(
        request.payload
    )

    for k, v in request.__dict__.items():
        assert v == request2.__dict__[k]
