"""
    Gateway result code
    ===================

    .. Copyright:
        Copyright 2019 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""

# flake8: noqa
from .proto.wp_global_pb2 import BLANK, PRESENT, PROCESS, SUCCESS, NEW, ERROR
from .proto.wp_global_pb2 import NO_OTAP, PROPAGATE_ONLY, PROPAGATE_AND_PROCESS, PROPAGATE_AND_PROCESS_WITH_DELAY, LEGACY_OTAP
from .proto.wp_global_pb2 import UNKNOWN_DELAY, TEN_MINUTES, THIRTY_MINUTES, ONE_HOUR, SIX_HOURS, ONE_DAY, TWO_DAYS, FIVE_DAYS

import enum


def parse_optional_field(message_obj, field, dic, key):
    """
    Copies attribute into dic if it exists in the proto message

    Args:
        message_obj (proto): protocol buffer object
        field (str): the field to test for existence in message_obj
        dic (dict): the dictionary where to copy the value into
        key (str): the dictionary key to use

    """

    if message_obj.HasField(field):
        dic[key] = getattr(message_obj, field)


def set_optional_field(message_obj, field, dic, key):
    """
    Sets field in the protocol buffer object. If the object does not
    accept it or if the key is not in dic the error is ignored.

    Args:
        message_obj (proto): protocol buffer object
        field (str): the field to test for existence in message_obj
        dic (dict): the dictionary where to copy the value into
        key (str): the dictionary key to use

    """

    try:
        setattr(message_obj, field, dic[key])
    except KeyError:
        # Field is unknown, just skip it
        pass


class ScratchpadType(enum.Enum):
    SCRATCHPAD_TYPE_BLANK = BLANK
    SCRATCHPAD_TYPE_PRESENT = PRESENT
    SCRATCHPAD_TYPE_PROCESS = PROCESS


class ScratchpadStatus(enum.Enum):
    SCRATCHPAD_STATUS_SUCCESS = SUCCESS
    SCRATCHPAD_STATUS_NEW = NEW
    SCRATCHPAD_STATUS_ERROR = ERROR


class ScratchpadAction(enum.Enum):
    ACTION_NO_OTAP = NO_OTAP
    ACTION_PROPAGATE_ONLY = PROPAGATE_ONLY
    ACTION_PROPAGATE_AND_PROCESS = PROPAGATE_AND_PROCESS
    ACTION_PROPAGATE_AND_PROCESS_WITH_DELAY = PROPAGATE_AND_PROCESS_WITH_DELAY
    ACTION_LEGACY_OTAP = LEGACY_OTAP


class ProcessingDelay(enum.Enum):
    DELAY_UNKNOWN = UNKNOWN_DELAY
    DELAY_TEN_MINUTES =  TEN_MINUTES
    DELAY_THIRTY_MINUTES = THIRTY_MINUTES
    DELAY_ONE_HOUR = ONE_HOUR
    DELAY_SIX_HOURS = SIX_HOURS
    DELAY_ONE_DAY = ONE_DAY
    DELAY_TWO_DAYS = TWO_DAYS
    DELAY_FIVE_DAYS = FIVE_DAYS


def parse_scratchpad_info(message_obj, dic):
    dic["len"] = message_obj.len
    dic["crc"] = message_obj.crc
    dic["seq"] = message_obj.seq


def set_scratchpad_info(message_obj, dic):
    message_obj.len = dic["len"]
    message_obj.crc = dic["crc"]
    message_obj.seq = dic["seq"]


def parse_scratchpad_target(message_obj, dic):
    dic["action"] = ScratchpadAction(message_obj.action)
    parse_optional_field(message_obj, "target_sequence", dic, "target_sequence")
    parse_optional_field(message_obj, "target_crc", dic, "target_crc")
    # Only one of the following will be set
    param = message_obj.WhichOneof("param")
    if param == "delay":
        dic["delay"] = ProcessingDelay(message_obj.delay)
    elif param == "raw":
        dic["param"] = message_obj.raw


def set_scratchpad_target(message_obj, dic):
    message_obj.action = dic["action"].value
    set_optional_field(message_obj, "target_sequence", dic, "target_sequence")
    set_optional_field(message_obj, "target_crc", dic, "target_crc")
    # Only one of the following key should be set
    try:
        message_obj.delay = dic["delay"].value
    except KeyError:
        # try the raw version
        set_optional_field(message_obj, "raw", dic, "param")
