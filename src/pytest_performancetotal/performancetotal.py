from typing import Generator
import pytest
# from typing import Type
from pytest_performancetotal.performance import Performance

@pytest.fixture
def performancetotal(request) -> Generator[Performance, None, None]:
    performance = Performance()
    print("Setup of function scoped fixture")
    yield performance
    print("Finalizing test with function scoped fixture")
    performance.finalize_test(request)
    

@pytest.fixture(scope='session', autouse=True)
def performance_worker(request: pytest.FixtureRequest) -> Generator[None, None, None]:
    performance = Performance()
    print("Initializing session scoped fixture")
    performance.initialize(request.config.rootdir)
    yield
    print("Analyzing using session scoped fixture")
    session_id = request.session.nodeid
    performance.analyze_results(session_id)
    
    