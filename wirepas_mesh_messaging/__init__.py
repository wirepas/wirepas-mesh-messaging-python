"""
    .. Copyright:
       Copyright 2019 Wirepas Ltd under Apache License, Version 2.0.
       See file LICENSE for full license details.
"""

from .__about__ import (
    __author__,
    __author_email__,
    __classifiers__,
    __copyright__,
    __description__,
    __license__,
    __pkg_name__,
    __title__,
    __url__,
    __version__,
    __keywords__,
    __warning_msg__,
)

from .get_configs import GetConfigsRequest, GetConfigsResponse
from .get_gw_info import GetGatewayInfoRequest, GetGatewayInfoResponse
from .set_config import SetConfigRequest, SetConfigResponse
from .received_data import ReceivedDataEvent
from .status import StatusEvent, GatewayState
from .send_data import SendDataRequest, SendDataResponse
from .upload_scratchpad import UploadScratchpadRequest, UploadScratchpadResponse
from .process_scratchpad import ProcessScratchpadRequest, ProcessScratchpadResponse
from .get_scratchpad_status import GetScratchpadStatusRequest, GetScratchpadStatusResponse
from .set_scratchpad_target import SetScratchpadTargetAndActionRequest, SetScratchpadTargetAndActionResponse
from .gateway_result_code import GatewayResultCode
from .otap_helper import ScratchpadStatus, ScratchpadType, ScratchpadAction, ProcessingDelay
from .wirepas_exceptions import GatewayAPIParsingException

from google.protobuf.internal import api_implementation

# pylint: disable=locally-disabled, protected-access, wrong-import-order
try:
    if api_implementation._default_implementation_type == "python":
        print(__warning_msg__)
except AttributeError:
    print("Could not evaluate protobuf implementation type")


__all__ = [
    "__author__",
    "__author_email__",
    "__classifiers__",
    "__copyright__",
    "__description__",
    "__license__",
    "__pkg_name__",
    "__title__",
    "__url__",
    "__version__",
    "__keywords__",
    "__warning_msg__",
]
