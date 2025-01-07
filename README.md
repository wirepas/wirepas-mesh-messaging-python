# Wirepas Mesh Messaging

This Python wheel contains the generated code to interact with Wirepas Mesh Network
through the Gateway to Backend API.
It offers an easy way to use the API in Python without the need to build the protobuf files yourself

## Installation

### Install from PyPi

This package is available from [PyPi][pypi].

```shell
    pip install wirepas-mesh-messaging
```

### From the source

This wheel can be built from source directly. You need to have [protobuf
compiler](https://grpc.io/docs/protoc-installation/) installed.

First, .proto files should be compiled
```shell
protoc -I backend-apis/gateway_to_backend/protocol_buffers_files/ \
    --python_out=./wirepas_mesh_messaging/proto \
     backend-apis/gateway_to_backend/protocol_buffers_files/*.proto
```

After that, the wheel can be built using [build](https://pypi.org/project/build/).
```shell
python3 -m build .
```

**Note:** When installing the package,
[protobuf](https://pypi.org/project/protobuf/) is installed automatically as a
dependency. On some environments (such as Alpine) the [recommended UPB
backend](https://github.com/protocolbuffers/protobuf/tree/main/python#implementation-backends)
might not available as a binary and the system might use the slower python
implementation. To get the UBP backend, you can configure pip to use the source
version of protobuf. This way the UPB backend would be built when installing
protobuf:
```shell
pip install . --no-binary protobuf
```
## Usage example

### Create a message to be sent to a Gateway in protobuf format

```python
>>> import wirepas_mesh_messaging as wmm

>>> downlink_message = wmm.SendDataRequest(dest_add=1234, src_ep=10, dst_ep=10, qos=0, payload=bytes.fromhex("0102ABCD"))

# downlink_message.payload can be published on right topic (protobuf formatted)
>>> downlink_message.payload
b'\n\x1e2\x1c\n\x0b\x08\x8e\xac\x9c\xbf\xab\x95\xbd\xf6\xfe\x01\x10\xd2\t\x18\n \n(\x002\x04\x01\x02\xab\xcd'


```
### Parse a Wirepas message received from a Gateway in protobuf format

```python
>>> import wirepas_mesh_messaging as wmm

# payload is the payload received from mqtt (protobuf formatted)
# Let's assume it was created like this on Gateway side:
# wmm.ReceivedDataEvent(gw_id="Gw1", sink_id="sink0", rx_time_ms_epoch=1608644981000, src=1234, dst=1, src_ep=10, dst_ep=10, travel_time_ms=128, qos=1).payload

>>> uplink_message = wmm.ReceivedDataEvent.from_payload(payload)

>>> print(uplink_message)
{'gw_id': 'Gw1', 'sink_id': 'sink0', 'event_id': 12527549978202166391, 'rx_time_ms_epoch': 1608644981000, 'source_address': 1234, 'destination_address': 1, 'source_endpoint': 10, 'destination_endpoint': 10, 'travel_time_ms': 128, 'qos': 1, 'data_payload': None, 'data_size': None, 'hop_count': 0}

```

## Services API documentation

Please refer to the [backend apis repository][github_backend_apis] for
documentation on the [Gateway to Backend API](https://github.com/wirepas/backend-apis/blob/scratchpad_target/gateway_to_backend/README.md).


## License

Licensed under the Apache License, Version 2.0.
See [LICENSE](LICENSE) for the full license text.

[pypi]: https://pypi.org/project/wirepas-messaging/

[github_backend_apis]: https://github.com/wirepas/backend-apis
