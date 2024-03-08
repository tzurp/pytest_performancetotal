from setuptools import find_packages, setup

setup(
    name='pytest-performancetotal',
    packages=['pytest_performancetotal'],
    package_dir={'pytest_performancetotal': 'src/pytest_performancetotal'},
    version='0.1b1',
    author='Tzur Paldi',
    author_email='tzur.paldi@outlook.com',
    maintainer='Tzur Paldi',
    maintainer_email='tzur.paldi@outlook.com',
    license='GNU',
    url='',
    description='A performance plugin for pytest',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
    ],
    entry_points={
        'pytest11': [
            'pytest_performancetotal = pytest_performancetotal.performancetotal',
        ],
    },
)
