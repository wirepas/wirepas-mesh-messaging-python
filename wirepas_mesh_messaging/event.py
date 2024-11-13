"""
    Event
    =====

    .. Copyright:
        Copyright 2019 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""
import random
import time

from .wirepas_message import WirepasMessage


class Event(WirepasMessage):
    """
    Event

    Attributes:
        gw_id (str): gateway unique identifier
        sink_id(str): sink identifier
        event_id(int): event unique id (random value generated if None)
        time_ms_epoch(int): timestamp in ms of event generation (0 to automatically set it, the default)
    """

    # pylint: disable=unused-argument
    def __init__(self, gw_id, sink_id=None, event_id=None, time_ms_epoch=0, **kwargs):

        super(Event, self).__init__()
        self.gw_id = gw_id
        self.sink_id = sink_id
        if event_id is None:
            event_id = random.getrandbits(64)
        self.event_id = event_id
        if time_ms_epoch == 0:
            time_ms_epoch = int(time.time() * 1000)
        self.time_ms_epoch = time_ms_epoch

    def __str__(self):
        return str(self.__dict__)

    def _load_event_header(self, event):
        header = event.header
        header.gw_id = str(self.gw_id)
        header.event_id = self.event_id

        if self.sink_id is not None:
            header.sink_id = str(self.sink_id)

        if self.time_ms_epoch is not None:
            header.time_ms_epoch = self.time_ms_epoch

    @staticmethod
    def _parse_event_header(header):
        """
        Parses the header details from a protobuff message

        Args:
            header (proto): proto buff message

        Returns:
            A dictionary with the header details
        """

        d = dict()
        d["gw_id"] = header.gw_id
        d["event_id"] = header.event_id
        if header.HasField("sink_id"):
            d["sink_id"] = header.sink_id
        else:
            d["sink_id"] = None

        if header.HasField("time_ms_epoch"):
            d["time_ms_epoch"] = header.time_ms_epoch
        else:
            d["time_ms_epoch"] = None

        return d
