# pytest-performancetotal

With this plugin for [pytest](https://github.com/pytest-dev/pytest) and for [playwright-pytest](https://github.com/microsoft/playwright-pytest) you can easily add performance analysis to any flow in your tests, whether it's a pure UI, API, or a combination of both. This plugin provides a simple and efficient way to measure the response times of various procedures and identify potential bottlenecks in your application. With this information, you can make informed decisions about optimizations and improvements to enhance the overall performance of your application. Read more in the TypeScript version article [here](https://www.linkedin.com/pulse/elevating-your-playwright-tests-plugin-tzur-paldi-phd).

## Installation

```no-highlight
$ pip install pytest-performancetotal
```

## Usage

To use pytest-performancetotal, simply add the **performancetotal** fixture to the test method. This will include the performance functionality in your test. No further setup is required. Here's an example:

```no-highlight
import pytest

@pytest.mark.parametrize("iteration", [1, 2, 3])
def test_features(performancetotal, iteration):
    performancetotal.sample_start("feature1")
    time.sleep(1)
    performancetotal.sample_end("feature1")
    
    performancetotal.sample_start("feature2")
    time.sleep(0.5)
    performancetotal.sample_end("feature2")
```

You can also get immediate time span for a single sample inside a test:

```no-highlight
feature1_timespan = performancetotal.get_sample_time("feature1")
```
be aware that get_sample_time returns a single measurement with no statistical analysis.


To use type hints follow this example:

```no-highlight
from pytest_performancetotal.performance import Performance

def test_features(performancetotal: Performance, iteration):
            # ... your test code here
```

## Options

To disable appending new results into existing file and start fresh every run use:
```no-highlight
pytest --performance-noappend
```

## Getting the results

A new directory named `performance_results` is created inside your project's root folder. Once all the tests are completed, two files are created inside the performance-results directory: `results.json` and `results.csv`. The analyzed data includes average time, standard error of mean (SEM), number of samples, minimum value, maximum value, earliest time, and latest time. The results table is also printed to the terminal log.

## Support

For any questions or suggestions contact me at: [tzur.paldi@outlook.com](mailto:tzur.paldi@outlook.com?subjet=pytest-performancetotal%20Support)