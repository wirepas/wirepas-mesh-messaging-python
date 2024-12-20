"""
    Received data
    =============

    .. Copyright:
        Copyright 2019 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""

from .proto import GenericMessage

from .event import Event


class ReceivedDataEvent(Event):
    """
    ReceivedDataEvent: Event generated when a message is received from Wirepas network

    Attributes:
        gw_id (str): gw_id (str): gateway unique identifier
        sink_id (str): id of the sink (dependant on gateway)
        rx_time_ms_epoch(int): timestamp in ms of message reception relative to epoch
        src(int): source address
        dst(int): destination address
        src_ep(int): source endpoint
        dst_ep(int): destination endpoint
        travel_time_ms(int): travel time of the packet in the Wirepas network
        qos(int): Wirepas QOS used by sender for this message
        data(bytearray): the received data or None if must be hidden
        data_size(int): the received data size, only needed if data is None
        event_id(int): event unique id (random value generated if None)
        hop_count(int): number of hop for the message to reach the gateway
        network_address(int): network_address of this message
    """

    def __init__(
        self,
        gw_id,
        sink_id,
        rx_time_ms_epoch,
        src,
        dst,
        src_ep,
        dst_ep,
        travel_time_ms,
        qos,
        data=None,
        data_size=None,
        event_id=None,
        hop_count=0,
        network_address=None,
        **kwargs
    ):
        super(ReceivedDataEvent, self).__init__(
            gw_id, sink_id, event_id=event_id, **kwargs
        )
        self.sink_id = sink_id
        self.rx_time_ms_epoch = rx_time_ms_epoch
        self.source_address = src
        self.destination_address = dst
        self.source_endpoint = src_ep
        self.destination_endpoint = dst_ep
        self.travel_time_ms = travel_time_ms
        self.qos = qos
        if data is not None:
            self.data_payload = bytes(data)
        else:
            self.data_payload = None

        self.data_size = data_size
        self.hop_count = hop_count
        self.network_address = network_address

    @staticmethod
    def _get_related_message(generic_message):
        return generic_message.wirepas.packet_received_event

    @classmethod
    def from_payload(cls, payload):
        event = cls._decode_and_get_related_message(payload)
        d = Event._parse_event_header(event.header)

        # Check optional hop count field
        try:
            hop_count = event.hop_count
        except AttributeError:
            # Attribute is not defined
            hop_count = 0

        # Check optional payload field
        if event.HasField("payload"):
            payload = event.payload
        else:
            payload = None

        # Check optional payload field
        if event.HasField("payload_size"):
            payload_size = event.payload_size
        else:
            # Attribute is not defined
            payload_size = None

        # Check optional network_address field
        if event.HasField("network_address"):
            network_address = event.network_address
        else:
            # Network address is not set
            network_address = None

        return cls(
            d["gw_id"],
            d["sink_id"],
            event.rx_time_ms_epoch,
            event.source_address,
            event.destination_address,
            event.source_endpoint,
            event.destination_endpoint,
            event.travel_time_ms,
            event.qos,
            data=payload,
            data_size=payload_size,
            event_id=d["event_id"],
            hop_count=hop_count,
            network_address=network_address,
            time_ms_epoch=d["time_ms_epoch"]
        )

    @property
    def payload(self):
        message = GenericMessage()
        # Fill the event header
        event = self._get_related_message(message)
        self._load_event_header(event)

        event.source_address = self.source_address
        event.destination_address = self.destination_address
        event.source_endpoint = self.source_endpoint
        event.destination_endpoint = self.destination_endpoint
        event.travel_time_ms = self.travel_time_ms
        event.rx_time_ms_epoch = self.rx_time_ms_epoch
        event.qos = self.qos

        if self.data_payload is not None:
            event.payload = self.data_payload

        if self.data_size is not None:
            event.payload_size = self.data_size

        if self.hop_count > 0:
            event.hop_count = self.hop_count

        if self.network_address is not None:
            event.network_address = self.network_address

        return message.SerializeToString()
