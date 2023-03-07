"""
    Status
    ======

    .. Copyright:
        Copyright 2019 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""

import enum
from .proto import GenericMessage, ON, OFF

from .event import Event
from .wirepas_exceptions import GatewayAPIParsingException

# Indicates that protobuf message definition in version 1 can be parsed by this implementation
# This API should never be changes in future (purpose of protobuf)
PB_MESSAGE_DEFINITION_VERSION = 1

from .config_helper import (
    parse_config_rw,
    parse_config_ro,
    parse_config_otap,
    set_config_ro,
    set_config_rw,
    set_config_otap
)

class GatewayState(enum.Enum):
    """
    GatewayState

    Enum providing the possible
    states for the gateway

    ONLINE or OFFLINE

    """

    ONLINE = 0
    OFFLINE = 1


class StatusEvent(Event):
    """
    StatusEvent: Event generated by the gateway to set its status (ONLINE/OFFLINE)

    Attributes:
        gw_id (str): gateway unique identifier
        state (GatewayState): state of the gateway
        version (int): protobuf messsage definition version for the gateway. This implementation can only parse protobuf message definitions in version1
        event_id(int): event unique id (random value generated if None)
        sink_configs (list): list of dictionnary containing the sink configs
        gateway_model (string): gateway model
        gateway_version (string): gateway version
    """

    def __init__(
        self,
        gw_id,
        state,
        version=PB_MESSAGE_DEFINITION_VERSION,
        event_id=None,
        sink_configs=[],
        gateway_model='',
        gateway_version='',
        **kwargs
    ):
        super(StatusEvent, self).__init__(gw_id, event_id=event_id, **kwargs)
        self.state = state
        self.version = version
        self.sink_configs = sink_configs
        self.gateway_model = gateway_model
        self.gateway_version = gateway_version

    @classmethod
    def from_payload(cls, payload):
        """ Converts a protobuff message into a python object """
        message = GenericMessage()
        try:
            message.ParseFromString(payload)
        except Exception:
            # Any Exception is promoted to Generic API exception
            raise GatewayAPIParsingException("Cannot parse StatusEvent payload")

        event = message.wirepas.status_event

        if event.state == ON:
            online = GatewayState.ONLINE
        else:
            online = GatewayState.OFFLINE

        if event.version != PB_MESSAGE_DEFINITION_VERSION:
            raise RuntimeError("Unsupported gateway message definition version. The only supported version is " + str(PB_MESSAGE_DEFINITION_VERSION))

        configs = []
        for conf in event.configs:
            config = {}

            config["sink_id"] = conf.sink_id

            parse_config_rw(conf, config)
            parse_config_ro(conf, config)
            parse_config_otap(conf, config)

            configs.append(config)

        d = Event._parse_event_header(event.header)
        return cls(d["gw_id"],
                   online,
                   event_id=d["event_id"],
                   sink_configs=configs,
                   time_ms_epoch=d["time_ms_epoch"],
                   gateway_model=event.gw_model,
                   gateway_version=event.gw_version)

    @property
    def payload(self):
        """ Returns a proto serialization of itself """

        message = GenericMessage()
        # Fill the request header
        status = message.wirepas.status_event
        self._load_event_header(status)

        status.version = PB_MESSAGE_DEFINITION_VERSION
        if self.state == GatewayState.ONLINE:
            status.state = ON
        else:
            status.state = OFF

        if self.sink_configs is not None:
            for config in self.sink_configs:
                conf = status.configs.add()
                conf.sink_id = config["sink_id"]

                set_config_rw(conf, config)
                set_config_ro(conf, config)
                set_config_otap(conf, config)

        if self.gateway_model is not None:
            status.gw_model = self.gateway_model

        if self.gateway_version is not None:
            status.gw_version = self.gateway_version

        return message.SerializeToString()
