"""
    Generic collection
    =============
    .. Copyright:
        Copyright 2020 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""
# flake8: noqa
from .wirepas_exceptions import GatewayAPIParsingException
from .proto import GenericMessage as protoGenericMessage
from .proto import GenericMessageCollection as protoGenericMessageCollection

import wirepas_mesh_messaging as wmm


class GenericCollection(object):
    """
    GenericCollection: collection of Generic message
    """

    field_to_class = {
        "packet_received_event": wmm.ReceivedDataEvent,
        "status_event": wmm.StatusEvent,
        "get_configs_req": wmm.GetConfigsRequest,
        "get_configs_resp": wmm.GetConfigsResponse,
        "set_config_req": wmm.SetConfigRequest,
        "set_config_resp": wmm.SetConfigResponse,
        "send_packet_req": wmm.SendDataRequest,
        "send_packet_resp": wmm.SendDataResponse,
        "get_scratchpad_status_req": wmm.GetScratchpadStatusRequest,
        "get_scratchpad_status_resp": wmm.GetScratchpadStatusResponse,
        "upload_scratchpad_req": wmm.UploadScratchpadRequest,
        "upload_scratchpad_resp": wmm.UploadScratchpadResponse,
        "process_scratchpad_req": wmm.ProcessScratchpadRequest,
        "process_scratchpad_resp": wmm.ProcessScratchpadResponse,
        "get_gateway_info_req": wmm.GetGatewayInfoRequest,
        "get_gateway_info_resp": wmm.GetGatewayInfoResponse,
        "set_scratchpad_target_and_action_req": wmm.SetScratchpadTargetAndActionRequest,
        "set_scratchpad_target_and_action_resp": wmm.SetScratchpadTargetAndActionResponse,
    }

    def __init__(self, generic_messages_list, **kwargs):
        self.generic_messages_list = generic_messages_list

    @classmethod
    def from_payload(cls, payload):
        message_collection = protoGenericMessageCollection()
        try:
            message_collection.ParseFromString(payload)
        except Exception:
            # Any Exception is promoted to Generic API exception
            raise GatewayAPIParsingException("Cannot parse Generic payload collection")

        msgs_list = []
        for message in message_collection.generic:
            for field, class_holder in GenericCollection.field_to_class.items():
                if message.wirepas.HasField(field):
                    msgs_list.append(class_holder.from_generic_message(message))
                    break

        return cls(msgs_list)

    @property
    def payload(self):
        message_collection = protoGenericMessageCollection()
        # Add all messages one by one
        for message in self.generic_messages_list:
            genMessage = protoGenericMessage()
            message_collection.generic.append(message.load_generic_message(genMessage))

        return message_collection.SerializeToString()

    @property
    def messages(self):
        return self.generic_messages_list

    def add_message(self, message):
        self.generic_messages_list.append(message)