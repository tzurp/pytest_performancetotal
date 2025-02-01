# pytest-performancetotal

With this plugin for [pytest](https://github.com/pytest-dev/pytest), which complements the [playwright-pytest](https://github.com/microsoft/playwright-pytest) integration, you can seamlessly incorporate performance analysis into your test flows. It’s designed to work with UI interactions, API calls, or a combination of both, providing a straightforward method for measuring response times and pinpointing potential performance issues within your application. By leveraging this data, you can make strategic decisions to optimize and enhance your application’s performance. For insights into the original concept and additional details, refer to the [article](https://www.linkedin.com/pulse/elevating-your-playwright-tests-plugin-tzur-paldi-phd) on the Node.js version of this plugin.

## Installation

```bash
$ pip install pytest-performancetotal
```

## Usage

To use pytest-performancetotal, simply add the **performancetotal** fixture to the test method. This will include the performance functionality in your test. No further setup is required. Here's an example:

```python
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

```python
feature1_timespan = performancetotal.get_sample_time("feature1")
```
be aware that get_sample_time returns a single measurement with no statistical analysis.


To use type hints follow this example:

```python
from pytest_performancetotal.performance import Performance

def test_features(performancetotal: Performance, iteration):
            # ... your test code here
```

### Options

#### __--performance-noappend__

To disable appending new results into existing file and start fresh every run use:

```bash
pytest --performance-noappend
```

> **⚠️ Caution:**
>
> This action will delete all your performance data permanently. Ensure that you have a backup before proceeding.

#### __--performance-drop-failed-results__

To drops results for failed tests use:

```bash
pytest --performance-drop-failed-results
```

#### __--performance-recent-days__

To set the umber of days to consider for performance analysis use:

`pytest --performance-recent-days=7` or use day portion like: `pytest --performance-recent-days=0.5`

#### __--performance-results-dir__

Set a custom results directory name/path:

On WIndows:

```bash
pytest --performance-results-dir=results\01012025
```

or

```bash
pytest --performance-results-dir=myCustomDir
```

On Linux:

```bash
pytest --performance-results-dir=results/01012025
```

or

```bash
pytest --performance-results-dir=myCustomDir
```

#### __--performance-results-file__

Set a custom results file name:

```bash
pytest --performance-results-file=myCustomFile
```

### Configuring Logging in pytest.ini

This plugin uses the native Python logging module to provide detailed logs during its execution. To ensure you can see these logs during testing, proper configuration is needed. The following instructions will guide you on how to configure pytest to output log messages to the console. This setup is particularly useful for debugging and tracking the behavior of your code.

Steps to Configure Logging:

Create or Update pytest.ini: If you do not already have a pytest.ini file, create one in the root directory of your project. If you have one, open it for editing.

For example add the following configuration in file `pytest.ini`:

```no-highlight
[pytest]
log_cli = true
log_cli_level = DEBUG # or INFO|WARNING|ERROR|CRITICAL
log_cli_format = %(asctime)s - %(name)s - %(levelname)s - %(message)s
log_cli_date_format = %Y-%m-%d %H:%M:%S
```

__log_cli__: Enables logging to the console.

__log_cli_level__: Sets the logging level. You can choose from DEBUG, INFO, WARNING, ERROR, or CRITICAL.

__log_cli_format__: Defines the format of the log messages.

__log_cli_date_format__: Specifies the date format used in log messages.

## Getting the results

A new directory named `performance_results` is created inside your project's root folder (unless you use a custom directory name). Once all the tests are completed, two files are created inside the performance-results directory: `results.json` and `results.csv`. The analyzed data includes average time, standard error of mean (SEM), number of samples, minimum value, maximum value, earliest time, and latest time. The results table is also printed to the terminal log.

### Analyzing performance data in bulk

To analyze existing performance data in bulk without generating new tests, it is recommended to use the [__performancetotal-cli__ tool](https://www.npmjs.com/package/performancetotal-cli). Although it is necessary to have Node.js, the tool can handle the results generated by __pytest-performancetotal__.

## Support

For any questions or suggestions contact me at: [tzur.paldi@outlook.com](mailto:tzur.paldi@outlook.com?subjet=pytest-performancetotal%20Support)