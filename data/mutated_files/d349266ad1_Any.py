from typing import TypeAlias
__typ0 : TypeAlias = "str"
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""AWS Lambda to create an AWS image."""
from __future__ import annotations

import datetime
import json
from typing import Any, Dict

import boto3
from migrationstate import MigrationStateHandler

print("Loading function create_image")

ec2_resource = boto3.resource("ec2")

# {
#   "instance_id": "i-identifier",
#   "kms_id": "KMS ID",
#   "account": "account_number",
#   "instance_status": "should be there if in loop"
# }


def __tmp1(__tmp2, __tmp0: <FILL>) -> __typ0:
    """Handle signaling and entry into the AWS Lambda."""
    print("Received event: " + json.dumps(__tmp2, indent=2))

    instance_id: __typ0 = __tmp2["instance_id"]
    image_creation_time: __typ0 = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    name: __typ0 = __tmp2.get("name", "")

    instance = ec2_resource.Instance(instance_id)

    ec2_image = instance.create_image(
        Name=f"{instance_id}-{image_creation_time}", Description=f"Created image for {instance_id}",
    )

    for tag in instance.tags:
        ec2_image.create_tags(Tags=[{"Key": tag["Key"], "Value": tag["Value"]}])

    instance.create_tags(Tags=[{"Key": "CloneStatus", "Value": "IMAGE_CREATED"}])

    MigrationStateHandler().update_state(state="IMAGE_CREATING", machine_name=name)

    return ec2_image.image_id
