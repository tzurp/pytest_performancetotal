from typing import Generator
import pytest
from pytest_performancetotal.performance import Performance

def pytest_addoption(parser: pytest.Parser):
    parser.addoption("--performance-noappend", action="store_true", default=False, help="Disables results appending to existing file. Previous data is deleted.")
    parser.addoption("--performance-drop-failed-results", action="store_true", default=False, help="Drops results for failed tests.")
    parser.addoption("--performance-recent-days", action="store", default=0, type=float, help="Number of days to consider for performance analysis.")
    
@pytest.fixture
def performancetotal(request) -> Generator[Performance, None, None]:
    performance = Performance()
    yield performance
    performance.finalize_test(request)

@pytest.fixture(scope='session', autouse=True)
def performance_worker(request: pytest.FixtureRequest) -> Generator[None, None, None]:
    performance = Performance()
    no_append = request.config.getoption('--performance-noappend', False)
    drop_results_for_failed = request.config.getoption('--performance-drop-failed-results', False)
    recent_days = request.config.getoption('--performance-recent-days', 0)  
    performance.initialize(request.config.rootdir, no_append)
    yield
    # session_id = request.session.nodeid
    performance.analyze_results(drop_results_for_failed, recent_days)
    
    