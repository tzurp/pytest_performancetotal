from typing import Generator
import pytest
from pytest_performancetotal.performance import Performance

def pytest_addoption(parser: pytest.Parser):
    parser.addoption("--performance-noappend", action='store_true', help='Disables results appending to existing file. Previous data is deleted.')
    
@pytest.fixture
def performancetotal(request) -> Generator[Performance, None, None]:
    performance = Performance()
    yield performance
    performance.finalize_test(request)

@pytest.fixture(scope='session', autouse=True)
def performance_worker(request: pytest.FixtureRequest) -> Generator[None, None, None]:
    performance = Performance()
    no_append = request.config.getoption('--performance-noappend', False)
    performance.initialize(request.config.rootdir, no_append)
    yield
    session_id = request.session.nodeid
    performance.analyze_results(session_id)
    
    