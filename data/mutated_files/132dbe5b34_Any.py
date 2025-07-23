from typing import TypeAlias
__typ0 : TypeAlias = "bool"
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""AWS Lambda to share an AWS image."""
from __future__ import annotations

import json
from typing import Any, Dict

import boto3
from migrationstate import MigrationStateHandler

print("Loading function share_image")

ec2_res = boto3.resource("ec2")

# {
#     "ami_id" : "ami-123456",
#     "kms_id"   : "GUID",
#     "wait_time": 60
# }


def __tmp1(__tmp2, __tmp0: <FILL>) :
    """Handle signaling and entry into the AWS Lambda."""
    print("Received event: " + json.dumps(__tmp2, indent=2))

    migrated_ami_id: str = __tmp2["migrated_ami_id"]
    instance_name: str = __tmp2.get("name", "")
    account: str = __tmp2["account"]

    # Access the image that needs to be copied
    image = ec2_res.Image(migrated_ami_id)

    try:
        # Share the image with the destination account
        image.modify_attribute(
            ImageId=image.id,
            Attribute="launchPermission",
            OperationType="add",
            LaunchPermission={"Add": [{"UserId": account}]},
        )
    except Exception as e:
        print(e)
        return False

    # We have to now share the snapshots associated with the AMI so it can be copied
    devices = image.block_device_mappings
    for device in devices:
        if "Ebs" in device:
            snapshot_id: str = device["Ebs"]["SnapshotId"]
            snapshot = ec2_res.Snapshot(snapshot_id)
            try:
                snapshot.modify_attribute(
                    Attribute="createVolumePermission",
                    CreateVolumePermission={"Add": [{"UserId": account}]},
                    OperationType="add",
                )
            except Exception as e:
                print(e)
                return False

    MigrationStateHandler().update_state(state="IMAGE_SHARED", machine_name=instance_name)
    return True
