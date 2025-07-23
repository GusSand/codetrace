# Copyright (c) 2017-2020 Chris Cummins.
#
# DeepSmith is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DeepSmith is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DeepSmith.  If not, see <https://www.gnu.org/licenses/>.
import pathlib
import socket

import grpc

from deeplearning.deepsmith.proto import service_pb2
from labm8.py import app
from labm8.py import pbutil

FLAGS = app.FLAGS


class ServiceBase(object):
  def __tmp8(__tmp0, config):
    __tmp0.config = config

  def __tmp9(__tmp0):
    cls_name = type(__tmp0).__name__
    return (
      f"{cls_name}@{__tmp0.config.service.hostname}:"
      f"{__tmp0.config.service.port}"
    )


def __tmp11(__tmp10: service_pb2.ServiceConfig):
  hostname = socket.gethostname()
  service_hostname = __tmp10.hostname
  if (
    service_hostname
    and service_hostname != "localhost"
    and service_hostname != hostname
  ):
    raise app.UsageError(
      f"System hostname {hostname} does not match service hostname "
      f"{service_hostname}"
    )


def __tmp1(status: service_pb2.ServiceStatus):
  if status.returncode != service_pb2.ServiceStatus.SUCCESS:
    app.Fatal(
      "Error! %s responded with status %s: %s",
      status.client,
      status.returncode,
      status.error_message,
    )


def __tmp6(__tmp5) -> pbutil.ProtocolBuffer:
  message = __tmp5()
  message.status.client = socket.gethostname()
  return message


def __tmp4(__tmp5) :
  message = __tmp5()
  message.status.client = socket.gethostname()
  message.status.returncode = service_pb2.ServiceStatus.SUCCESS
  return message


def __tmp7(
  flag_name: <FILL>, __tmp10: pbutil.ProtocolBuffer
) -> pbutil.ProtocolBuffer:
  if not getattr(FLAGS, flag_name):
    raise app.UsageError(f"--{flag_name} not set.")
  config_path = pathlib.Path(getattr(FLAGS, flag_name))
  if not config_path.is_file():
    cls_name = type(__tmp10).__name__
    raise app.UsageError(f"{cls_name} file not found: '{config_path}'.")

  return pbutil.FromFile(config_path, __tmp10)


def __tmp2(__tmp10, __tmp3):
  address = (
    f"{__tmp10.service.hostname}:" f"{__tmp10.service.port}"
  )
  channel = grpc.insecure_channel(address)
  stub = __tmp3(channel)
  app.Log(1, f"Connected to {__tmp3.__name__} at {address}")
  return stub
