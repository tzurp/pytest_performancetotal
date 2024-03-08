import re
import time
from playwright.sync_api import Page, expect
from pytest_performancetotal.performancetotal import Performance


def test_has_title(performancetotal: Performance):
    print("Starting test test_has_title...")
    performancetotal.sampleStart("startup1")
    time.sleep(1.5)
    performancetotal.sampleEnd("startup1")
    
    
    
