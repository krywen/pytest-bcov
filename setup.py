from setuptools import setup

setup(
    name='pytest-bcov',
    version='0.1',
    packages=['bcov'],
    entry_points={
        'pytest11': [
            'bcov = bcov.plugin',
        ],
    },
    install_requires=['pytest>=6.0.0'],
)