from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='pytest-performancetotal',
    packages=find_packages(where='src', exclude=['*tests*']),
    package_dir={'': 'src'},
    version='0.2',
    author='Tzur Paldi',
    author_email='tzur.paldi@outlook.com',
    maintainer='Tzur Paldi',
    maintainer_email='tzur.paldi@outlook.com',
    license='GNU',
    url='',
    description='A performance plugin for pytest',
    keywords='pytest plugin performance playwright',
    long_description=long_description,
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
    install_requires=[
        'filelock>=3.13.0',
    ]
)
