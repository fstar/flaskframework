from unittest import mock
import pytest


@pytest.fixture(scope='session', autouse=True)
@mock.patch('sk_grpc_client.case.UniverseCaseClient.update_case', return_value=None)
@mock.patch('sk_grpc_client.case.UniverseCaseClient.get_case', return_value=None)
def universe_client(func_1, func_2):  # pylint: disable=W0613
    return None
