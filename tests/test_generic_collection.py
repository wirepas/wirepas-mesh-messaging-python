# flake8: noqa

import wirepas_mesh_messaging
from default_value import *
import time


def test_generate_parse_collection():

    event1 = wirepas_mesh_messaging.ReceivedDataEvent(
        GATEWAY_ID,
        SINK_ID,
        RX_TIME_MS_EPOCH,
        SOURCE_ADD,
        DESTINATION_ADD,
        SOURCE_EP,
        DESTINATION_EP,
        TRAVEL_TIME_MS,
        QOS,
        DATA_PAYLOAD,
        hop_count=HOP_COUNT,
    )

    event2 = wirepas_mesh_messaging.ReceivedDataEvent(
        GATEWAY_ID,
        SINK_ID,
        RX_TIME_MS_EPOCH + 10,
        SOURCE_ADD,
        DESTINATION_ADD,
        SOURCE_EP,
        DESTINATION_EP,
        TRAVEL_TIME_MS,
        QOS,
        DATA_PAYLOAD,
        hop_count=HOP_COUNT,
    )

    request = wirepas_mesh_messaging.GetGatewayInfoRequest(REQUEST_ID)

    response = wirepas_mesh_messaging.GetGatewayInfoResponse(
        REQUEST_ID,
        GATEWAY_ID,
        RES_OK,
        int(time.time()),
        "Gateway model A",
        "Version x.y",
        implemented_api_version=IMPLEMENTED_API_VERSION,
    )

    message_list = [event1, request, event2, response]

    collection = wirepas_mesh_messaging.GenericCollection(message_list)

    collection2 = wirepas_mesh_messaging.GenericCollection.from_payload(collection.payload)

    message_list_2 = collection2.messages
    # Compare then one by one after serialization (order should be kept)
    for i in range(len(message_list)):
        assert(message_list[i].payload == message_list_2[i].payload)

