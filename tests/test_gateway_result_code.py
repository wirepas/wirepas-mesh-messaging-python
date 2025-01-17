# flake8: noqa

import pytest

from wirepas_mesh_messaging.proto import ErrorCode
from wirepas_mesh_messaging import GatewayResultCode

@pytest.mark.parametrize("protobuf_result_code", ErrorCode.items())
def test_decoding_errors(protobuf_result_code):
    name, value = protobuf_result_code
    try:
        GatewayResultCode(value)
    except ValueError as e:
        raise ValueError(f"{name} is not defined in GatewayResultCode") from e

