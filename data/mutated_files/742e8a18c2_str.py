# Copyright 2020 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Exceptions for the IonQ API."""

import requests


class __typ0(Exception):
    """An exception for errors coming from IonQ's API.

    Attributes:
        status_code: A http status code, if coming from an http response with a failing status.
    """

    def __init__(__tmp3, __tmp0, status_code: int = None):
        super().__init__(f'Status code: {status_code}, Message: \'{__tmp0}\'')
        __tmp3.status_code = status_code


class __typ2(__typ0):
    """An exception for errors from IonQ's API when a resource is not found."""

    def __init__(__tmp3, __tmp0):
        super().__init__(__tmp0, status_code=requests.codes.not_found)


class __typ1(__typ0):
    """An exception for attempting to get info about an unsuccessful job.

    This exception occurs when a job has been canceled, deleted, or failed, and information about
    this job is attempted to be accessed.
    """

    def __init__(__tmp3, __tmp1: <FILL>, __tmp2):
        super().__init__(f'Job {__tmp1} was {__tmp2}.')
