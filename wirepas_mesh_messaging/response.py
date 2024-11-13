"""
    Response
    ========

    .. Copyright:
        Copyright 2019 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""

import time

from .gateway_result_code import GatewayResultCode
from .wirepas_message import WirepasMessage


class Response(WirepasMessage):
    """
    Response

    Attributes:
        gw_id (str): unique gateway identifier
        sink_id(str): sink identifier
        req_id (int): identifier to help distinguish a response/request pair (same as in request)
        res(GatewayResultCode): result of the operation
        time_ms_epoch(int): timestamp in ms of response generation (0 to automatically set it, the default)
    """

    # pylint: disable=unused-argument
    def __init__(self, req_id, gw_id, res, sink_id=None, time_ms_epoch=0, **kwargs):
        super(Response, self).__init__()
        self.gw_id = gw_id
        self.sink_id = sink_id
        self.req_id = req_id
        self.res = res
        if time_ms_epoch == 0:
            time_ms_epoch = int(time.time() * 1000)
        self.time_ms_epoch = time_ms_epoch

    def __str__(self):
        return str(self.__dict__)

    def _load_response_header(self, response):
        """ Creates the generic messaging header """
        header = response.header
        header.req_id = self.req_id
        header.gw_id = str(self.gw_id)
        # No conversion needed as one to one mapping
        header.res = self.res.value

        if self.sink_id is not None:
            header.sink_id = str(self.sink_id)

        if self.time_ms_epoch is not None:
            header.time_ms_epoch = self.time_ms_epoch

    @staticmethod
    def _parse_response_header(header):
        """
        Parses the header details from a protobuff message

        Args:
            header (proto): proto buff message

        Returns:
            A dictionary with the header details
        """
        d = dict()
        d["req_id"] = header.req_id
        d["gw_id"] = header.gw_id
        d["res"] = GatewayResultCode(header.res)

        if header.HasField("sink_id"):
            d["sink_id"] = header.sink_id
        else:
            d["sink_id"] = None

        if header.HasField("time_ms_epoch"):
            d["time_ms_epoch"] = header.time_ms_epoch
        else:
            d["time_ms_epoch"] = None

        return d
