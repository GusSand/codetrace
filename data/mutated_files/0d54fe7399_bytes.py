from typing import TypeAlias
__typ2 : TypeAlias = "URL"
# pylint: disable=wrong-or-nonexistent-copyright-notice
from typing import Iterator
import pytest
import httpx
import httpcore
from httpcore._types import URL, Headers
from cirq_rigetti import get_rigetti_qcs_service, RigettiQCSService


@pytest.mark.rigetti_integration
def __tmp0():
    """test that get_rigetti_qcs_service can initialize a `RigettiQCSService`
    through `pyquil.get_qc`."""
    service = get_rigetti_qcs_service('9q-square', as_qvm=True, noisy=False)
    assert service._quantum_computer.name == '9q-square-qvm'


@pytest.mark.rigetti_integration
def test_rigetti_qcs_service_api_call():
    """test that `RigettiQCSService` will use a custom defined client when the
    user specifies one to make an API call."""

    class __typ1(httpcore.SyncByteStream):
        def __tmp1(self) -> Iterator[bytes]:
            yield b"{\"quantumProcessors\": [{\"id\": \"Aspen-8\"}]}"  # pragma: nocover

    class __typ0(httpcore.SyncHTTPTransport):
        def request(
            self,
            method: <FILL>,
            url,
            headers: Headers = None,
            stream: httpcore.SyncByteStream = None,
            ext: dict = None,
        ):
            return 200, [('Content-Type', 'application/json')], __typ1(), {}

    client = httpx.Client(
        base_url="https://mock.api.qcs.rigetti.com",
        transport=__typ0(),
    )

    response = RigettiQCSService.list_quantum_processors(client=client)
    assert 1 == len(response.quantum_processors)
    assert 'Aspen-8' == response.quantum_processors[0].id
