from typing import Generator
import pytest
from pytest_performancetotal.performance import Performance

def pytest_addoption(parser: pytest.Parser):
    parser.addoption("--performance-noappend", action="store_true", default=False, help="Disables results appending to existing file. Previous data is deleted.")
    parser.addoption("--performance-drop-failed-results", action="store_true", default=False, help="Drops results for failed tests.")
    parser.addoption("--performance-recent-days", action="store", default=0, type=float, help="Number of days to consider for performance analysis.")
    parser.addoption("--performance-results-dir", action="store", default="performance_results", type=str, help="Performance results directory name.")
    parser.addoption("--performance-results-file", action="store", default="results", type=str, help="Performance results file name.")
    
@pytest.fixture
def performancetotal(request) -> Generator[Performance, None, None]:
    performance = Performance(request)
    yield performance
    performance.finalize_test()

@pytest.fixture(scope='session', autouse=True)
def performance_worker(request: pytest.FixtureRequest) -> Generator[None, None, None]:
    performance = Performance(request)
    performance.initialize()
    yield
    # session_id = request.session.nodeid
    performance.analyze_results()
    
    