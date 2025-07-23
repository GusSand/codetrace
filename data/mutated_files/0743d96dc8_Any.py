from typing import TypeAlias
__typ0 : TypeAlias = "str"
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""AWS Lambda to copy an AWS image."""
from __future__ import annotations

import json
import os
from typing import Any, Dict

import boto3
from migrationstate import MigrationState, MigrationStateHandler

print("Loading function copy_image")

# {
#     "ami_id"    : "ami-123456",
#     "kms_id"    : "GUID",
#     "wait_time" : 60,
#     "region"    : "optional destination region"
# }


def __tmp0(event, context: <FILL>) :
    """Handle signaling and entry into the AWS Lambda."""
    print("Received event: " + json.dumps(event, indent=2))

    migrated_ami_id: __typ0 = event["migrated_ami_id"]
    kms_id: __typ0 = event["kms_id"]
    region: __typ0 = event.get("region", os.environ.get("AWS_REGION"))
    role: __typ0 = event.get("role")
    instance_name: __typ0 = event.get("name", "")

    sts_client = boto3.client("sts")

    print(f"Assuming role: {role}")
    assumed_role: Dict[__typ0, Any] = sts_client.assume_role(RoleArn=role, RoleSessionName="CopyImageLambda")

    credentials = assumed_role.get("Credentials")

    ec2_client = boto3.client(
        "ec2",
        region_name=region,
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"],
    )

    try:
        new_image: Dict[__typ0, Any] = ec2_client.copy_image(
            SourceImageId=migrated_ami_id,
            SourceRegion=region,
            Name=f"copied-{migrated_ami_id}",
            Encrypted=True,
            KmsKeyId=kms_id,
        )
    except Exception as e:
        print(e)
        return ""

    MigrationStateHandler().update_state(state="IMAGE_COPYING", machine_name=instance_name)
    return new_image.get("ImageId", "")
