import pytest
def pytest_addoption(parser):
    parser.addoption(
        '--token', action='store', default='none', help='Token to acces WEBAPI BPS'
    )
    
@pytest.fixture
def token(request):
    token = request.config.getoption('--token')
    return token
