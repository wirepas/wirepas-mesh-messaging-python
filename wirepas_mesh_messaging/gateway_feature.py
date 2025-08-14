"""
    Gateway feature
    ==========

    .. Copyright:
        Copyright 2025 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""

import enum
from .proto import GatewayFeature as GatewayFeature_pb

class GatewayFeature(enum.Enum):
    """
    Class that represent all possible gateway feature flags.
    Keep a one-to-one mapping with current protobuf flags to ease conversion.
    """

    GW_FEATURE_UNKNOWN = GatewayFeature_pb.UNKNOWN
    GW_FEATURE_SCRATCHPAD_CHUNK_V1 = GatewayFeature_pb.SCRATCHPAD_CHUNK_V1
    GW_FEATURE_CONFIGURATION_DATA_V1 = GatewayFeature_pb.CONFIGURATION_DATA_V1
    GW_FEATURE_SINK_KEY_MANAGEMENT_V1 = GatewayFeature_pb.SINK_KEY_MANAGEMENT_V1

