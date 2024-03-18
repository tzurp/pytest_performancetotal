# pytest-performancetotal

With this plugin for [pytest](https://github.com/pytest-dev/pytest), which complements the [playwright-pytest](https://github.com/microsoft/playwright-pytest) integration, you can seamlessly incorporate performance analysis into your test flows. It’s designed to work with UI interactions, API calls, or a combination of both, providing a straightforward method for measuring response times and pinpointing potential performance issues within your application. By leveraging this data, you can make strategic decisions to optimize and enhance your application’s performance. For insights into the original concept and additional details, refer to the [article](https://www.linkedin.com/pulse/elevating-your-playwright-tests-plugin-tzur-paldi-phd) on the Node.js version of this plugin.

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