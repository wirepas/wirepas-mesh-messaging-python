import sys, os
sys.path.append(os.path.dirname(__file__))

# Protobuf files will be compiled here
from .error_pb2 import *
from .wp_global_pb2 import *
from .config_message_pb2 import *
from .otap_message_pb2 import *
from .generic_message_pb2 import *
from .data_message_pb2 import *