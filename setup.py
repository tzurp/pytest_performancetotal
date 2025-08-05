from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='pytest-performancetotal',
    packages=find_packages(where='src', exclude=['*tests*']),
    package_dir={'': 'src'},
    version='0.2.11',
    author='Tzur Paldi',
    author_email='tzur.paldi@outlook.com',
    maintainer='Tzur Paldi',
    maintainer_email='tzur.paldi@outlook.com',
    license='Apache-2.0',
    url='https://github.com/tzurp/pytest_performancetotal',
    project_urls={
        "Bug Tracker": "https://github.com/tzurp/pytest_performancetotal/issues",
        "Documentation": "https://github.com/tzurp/pytest_performancetotal#readme",
        "Source Code": "https://github.com/tzurp/pytest_performancetotal"
    },
    description='A performance plugin for pytest',
    keywords='pytest plugin performance playwright',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Pytest",
        "License :: OSI Approved :: Apache Software License"
    ],
    license_files=["LICENSE"],
    entry_points={
        'pytest11': [
            'pytest_performancetotal = pytest_performancetotal.performancetotal',
        ],
    },
    install_requires=[
        'filelock>=3.13.0',
    ]
)
