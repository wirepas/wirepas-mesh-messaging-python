# flake8: noqa

import pytest

import wirepas_mesh_messaging
from wirepas_mesh_messaging.proto import GenericMessage
from wirepas_mesh_messaging.wirepas_exceptions import (
    GatewayAPIParsingException,
    InvalidMessageType,
)

MESSAGE_CLASSES = [
    wirepas_mesh_messaging.GetConfigsRequest,
    wirepas_mesh_messaging.GetConfigsResponse,
    wirepas_mesh_messaging.GetGatewayInfoRequest,
    wirepas_mesh_messaging.GetGatewayInfoResponse,
    wirepas_mesh_messaging.GetScratchpadStatusRequest,
    wirepas_mesh_messaging.GetScratchpadStatusResponse,
    wirepas_mesh_messaging.ProcessScratchpadRequest,
    wirepas_mesh_messaging.ProcessScratchpadResponse,
    wirepas_mesh_messaging.ReceivedDataEvent,
    wirepas_mesh_messaging.SendDataRequest,
    wirepas_mesh_messaging.SendDataResponse,
    wirepas_mesh_messaging.SetConfigRequest,
    wirepas_mesh_messaging.SetConfigResponse,
    wirepas_mesh_messaging.SetScratchpadTargetAndActionRequest,
    wirepas_mesh_messaging.SetScratchpadTargetAndActionResponse,
    wirepas_mesh_messaging.StatusEvent,
    wirepas_mesh_messaging.UploadScratchpadRequest,
    wirepas_mesh_messaging.UploadScratchpadResponse,
]


def _get_payload_excluding_message_type(message_class):
    if message_class == wirepas_mesh_messaging.GetConfigsRequest:
        return wirepas_mesh_messaging.GetGatewayInfoRequest().payload

    return wirepas_mesh_messaging.GetConfigsRequest().payload


@pytest.mark.parametrize("message_class", MESSAGE_CLASSES)
def test_decoding_errors(message_class):
    invalid_protobuf_message = bytes([0])

    with pytest.raises(GatewayAPIParsingException, match="Cannot decode"):
        message_class.from_payload(invalid_protobuf_message)


@pytest.mark.parametrize("message_class", MESSAGE_CLASSES)
def test_decoding_wrong_message_type(message_class):
    payload = _get_payload_excluding_message_type(message_class)

    with pytest.raises(InvalidMessageType, match=message_class.__name__):
        message_class.from_payload(payload)


@pytest.mark.parametrize("message_class", MESSAGE_CLASSES)
def test_decoding_missing_message_type(message_class):
    message = GenericMessage()
    message.wirepas.SetInParent()
    payload = message.SerializeToString()

    with pytest.raises(InvalidMessageType, match=message_class.__name__):
        message_class.from_payload(payload)
