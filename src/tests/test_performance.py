import pytest
import random
import time
from playwright.sync_api import Page
from pytest_performancetotal.performancetotal import Performance

# @pytest.mark.skip(reason="too long")
@pytest.mark.parametrize("iteration", [1, 2, 3])
def test_startup_performance(page: Page, performancetotal: Performance, iteration):
    globalTimeout: 5 * 60 * 1000 # type: ignore
    print(f"iteration: {iteration}")
    page.goto("http://www.microsoft.com")
    performancetotal.sample_start("startup_SF")
    page.goto('https://sourceforge.net/')
    performancetotal.sample_end("startup_SF")

    performancetotal.sample_start("startup_GH")
    page.goto('http://github.com/')
    performancetotal.sample_end("startup_GH")

    message = "GitHub is faster" if performancetotal.get_sample_time("startup_GH") < performancetotal.get_sample_time("startup_SF") else "SourceForge is faster"

    print(message)

@pytest.mark.parametrize("iteration", [1, 2, 3])
def test_features(performancetotal: Performance, iteration):
    print(f"Starting test_features iteration {iteration}")
    
    performancetotal.sample_start("feature1")
    
    time.sleep(1 + random.uniform(-0.5, 0.5))
    
    performancetotal.sample_end("feature1")
    
    performancetotal.sample_start("feature2")
    
    time.sleep(1 + random.uniform(-0.5, 0.5))
    
    performancetotal.sample_end("feature2")

    