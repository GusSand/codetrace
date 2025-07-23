# Copyright 2018 The Cirq Developers
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

from typing import Optional

import requests


class __typ0:
    """Details how to access a repository on github."""

    def __init__(__tmp0, organization, name: <FILL>, access_token) :
        """Inits GithubRepository.

        Args:
            organization: The github organization the repository is under.
            name: The name of the github repository.
            access_token: If present, this token is used to authorize changes
                to the repository when calling the github API (e.g. set build
                status indicators). Avoid using access tokens with more
                permissions than necessary.
        """
        __tmp0.organization = organization
        __tmp0.name = name
        __tmp0.access_token = access_token

    def __tmp1(__tmp0) :
        """Returns a string identifying the location of this repository."""
        return f'git@github.com:{__tmp0.organization}/{__tmp0.name}.git'

    def delete(__tmp0, __tmp2, **kwargs):
        return requests.delete(__tmp2, **__tmp0._auth(kwargs))

    def get(__tmp0, __tmp2, **kwargs):
        return requests.get(__tmp2, **__tmp0._auth(kwargs))

    def put(__tmp0, __tmp2, **kwargs):
        return requests.put(__tmp2, **__tmp0._auth(kwargs))

    def post(__tmp0, __tmp2, **kwargs):
        return requests.post(__tmp2, **__tmp0._auth(kwargs))

    def patch(__tmp0, __tmp2, **kwargs):
        return requests.patch(__tmp2, **__tmp0._auth(kwargs))

    def _auth(__tmp0, kwargs):
        new_kwargs = kwargs.copy()
        headers = kwargs.get('headers', {})
        headers.update({"Authorization": f"token {__tmp0.access_token}"})
        new_kwargs.update(headers=headers)
        return new_kwargs
