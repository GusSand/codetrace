from typing import TypeAlias
__typ0 : TypeAlias = "str"
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Check the state of an AWS AMI."""
from __future__ import annotations

import json
from typing import Any, Dict

import boto3
from migrationstate import MigrationStateHandler

print("Loading function get_image_status")

ec2_client = boto3.client("ec2")

# {
#   "instance_id": "i-identifier",
#   "kms_id": "KMS ID",
#   "account": "account_number",
#   "instance_status": "should be there if in loop"
#   "migrated_ami_id": "ami-identifier"
# }


def __tmp0(event, context: <FILL>) :
    """Handle signaling and entry into the AWS Lambda."""
    print("Received event: " + json.dumps(event, indent=2))

    migrated_ami_id: __typ0 = event["migrated_ami_id"]
    instance_name: __typ0 = event.get("name", "")

    ami_state: Dict[__typ0, Any] = ec2_client.describe_images(ImageIds=[migrated_ami_id])

    state = ami_state["Images"][0]["State"]
    if state == "available":
        MigrationStateHandler().update_state(state="IMAGE_CREATED", machine_name=instance_name)

    return state
