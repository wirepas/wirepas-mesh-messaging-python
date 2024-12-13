import base64


def get_cdc_with_base64(cdc):
    """
    Bytes objects are base64 encoded in protobuf JSON format.
    Payload fields should be base64 encoded in that case.
    """
    cdc_with_base64 = []
    for cdc_item in cdc:
        cdc_with_base64.append(
            {
                "endpoint": cdc_item["endpoint"],
                "payload": base64.b64encode(cdc_item["payload"]),
            }
        )
    return cdc_with_base64
