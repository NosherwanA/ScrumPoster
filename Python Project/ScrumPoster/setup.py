#!/usr/bin/env python

from pip.req import parse_requirements
from pip.download import PipSession
from setuptools import setup

session = PipSession()

packages = [
            'ScrumPoster',
            ]

install_reqs = parse_requirements('requirements.txt', session=session)

setup(
    name='ScrumPoster',
    version='1.0',
    packages=packages,
    description=""""ScrumPoster""",
    long_description="Posts scrum message in multiple channels",
    author="Nosherwan Ahmed",
    author_email='nosherwan.a2@gmail.com',
    url="https://github.com/NosherwanA",
    package_dir={'ScrumPoster': 'ScrumPoster'},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'ScrumPoster = ScrumPoster.ScrumPoster:main'
        ]
    },
    classifiers=(
        'Programming Language :: Python :: 3.5',
    ),
    install_requires=[str(r.req) for r in install_reqs],
)