# flake8: noqa

import pytest
import wirepas_mesh_messaging
from wirepas_mesh_messaging.proto import GatewayFeature as GatewayFeature_pb

@pytest.mark.parametrize("protobuf_feature_flag", GatewayFeature_pb.items())
def test_decoding_errors(protobuf_feature_flag):
    """
    Make sure all the feature flags in the internal
    (wirepas_mesh_messaging.OptionalGatewayFeature) enum are aligned with the
    protobuf side if the protobuf definition is updated in this library.
    """

    name, value = protobuf_feature_flag
    try:
        wirepas_mesh_messaging.GatewayFeature(value)
    except ValueError as e:
        raise ValueError(f"{name} is not defined in GatewayFeature") from e

