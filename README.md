# pytest-performancetotal

This plugin for [pytest](https://github.com/pytest-dev/pytest) and for [playwright-pytest](https://github.com/microsoft/playwright-pytest)

## Installation

```no-highlight
$ pip install pytest-performancetotal
```

## Usage

To use pytest-performancetotal, simply add the **performancetotal** fixture to the test method. This will include the performance functionality in your test. No further setup is required. Here's an example:

```no-highlight
def test_performance(performancetotal):
            # ...

            # ...
```

To use type hints follow this example:

```no-highlight
from pytest_performancetotal.performance import performance

def test_performance(performancetotal:performance):
            # ... your test code here
```

## Support

For any questions or suggestions contact me at: [tzur.paldi@outlook.com](mailto:tzur.paldi@outlook.com?subjet=pytest-performancetotal%20Support)