"""
    Get configs
    ===========

    .. Copyright:
        Copyright 2019 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""

from .proto import GenericMessage

from .request import Request
from .response import Response

from .config_helper import (
    parse_config_rw,
    parse_config_ro,
    parse_config_otap,
    set_config_ro,
    set_config_rw,
    set_config_otap,
)


class GetConfigsRequest(Request):
    """
    GetConfigsRequest: Request to obtain the configs of all sinks from a gateway

    Attributes:
        req_id (int): unique request id
    """

    def __init__(self, req_id=None, **kwargs):
        super(GetConfigsRequest, self).__init__(req_id=req_id, **kwargs)

    @staticmethod
    def _get_related_message(generic_message):
        return generic_message.wirepas.get_configs_req

    @classmethod
    def from_payload(cls, payload):
        req = cls._decode_and_get_related_message(payload)

        d = Request._parse_request_header(req.header)
        return cls(d["req_id"], time_ms_epoch=d["time_ms_epoch"])

    @property
    def payload(self):
        message = GenericMessage()
        # Fill the request header
        get_config = self._get_related_message(message)
        self._load_request_header(get_config)

        return message.SerializeToString()


class GetConfigsResponse(Response):
    """
    GetConfigsResponse: Response to answer a GetConfigsRequest

    Attributes:
        req_id (int): unique request id that this Response is associated
        gw_id (str): gw_id (str): gateway unique identifier
        res (GatewayResultCode): result of the operation
        configs (list): list of dictionnary containing a dict representing an attached sink
    """

    def __init__(self, req_id, gw_id, res, configs, **kwargs):
        super(GetConfigsResponse, self).__init__(req_id, gw_id, res, **kwargs)
        self.configs = configs

    @staticmethod
    def _get_related_message(generic_message):
        return generic_message.wirepas.get_configs_resp

    @classmethod
    def from_payload(cls, payload):
        response = cls._decode_and_get_related_message(payload)

        d = Response._parse_response_header(response.header)

        configs = []

        for conf in response.configs:
            config = {}

            config["sink_id"] = conf.sink_id

            parse_config_rw(conf, config)
            parse_config_ro(conf, config)
            parse_config_otap(conf, config)

            configs.append(config)

        return cls(d["req_id"], d["gw_id"], d["res"], configs, time_ms_epoch=d["time_ms_epoch"])

    @property
    def payload(self):
        message = GenericMessage()

        response = self._get_related_message(message)
        self._load_response_header(response)

        for config in self.configs:
            conf = response.configs.add()
            conf.sink_id = config["sink_id"]

            set_config_rw(conf, config)
            set_config_ro(conf, config)
            set_config_otap(conf, config)

        return message.SerializeToString()
