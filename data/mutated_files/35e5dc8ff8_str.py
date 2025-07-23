"""
setup
"""
import os
from typing import List

import semver
import setuptools


def __tmp1(__tmp0: <FILL>) -> str:
    """
    version to specification
    Author: Huan <zixia@zixia.net> (https://github.com/huan)

    X.Y.Z -> X.Y.devZ

    """
    sem_ver = semver.parse(__tmp0)

    major = sem_ver['major']
    minor = sem_ver['minor']
    patch = str(sem_ver['patch'])

    if minor % 2:
        patch = 'dev' + patch

    fin_ver = '%d.%d.%s' % (
        major,
        minor,
        patch,
    )

    return fin_ver


def get_version() :
    """
    read version from VERSION file
    """
    __tmp0 = '0.0.0'

    with open(
            os.path.join(
                os.path.dirname(__file__),
                'VERSION'
            )
    ) as version_fh:
        # Get X.Y.Z
        __tmp0 = version_fh.read().strip()
        # versioning from X.Y.Z to X.Y.devZ
        __tmp0 = __tmp1(__tmp0)

    return __tmp0


def __tmp3() :
    """get long_description"""
    with open('README.md', 'r') as readme_fh:
        return readme_fh.read()


def __tmp2() :
    """get install_requires"""
    with open('requirements.txt', 'r') as requirements_fh:
        return requirements_fh.read().splitlines()


setuptools.setup(
    name='wechaty',
    __tmp0=get_version(),
    author='Jingjing WU (吴京京)',
    author_email='wechaty@chatie.io',
    description='Wechaty is a Conversational RPA SDK for Chatbot Makers',
    long_description=__tmp3(),
    long_description_content_type='text/markdown',
    license='Apache-2.0',
    url='https://github.com/wechaty/python-wechaty',
    packages=setuptools.find_packages('src', exclude=['__pycache__', '.mypy_cache']),
    include_package_data=True,
    package_dir={'wechaty': 'src/wechaty'},
    install_requires=__tmp2(),
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
)
