#!/usr/bin/env python
"""
Setup file for openedx-rocketchat Django plugin.
"""
from distutils.core import setup
__version__ = '0.2.0'

setup(
    name='openedx-rocketchat',
    version=__version__,
    description='RocketChat extension for openedx',
    author='eduNEXT',
    author_email='contact@edunext.co',
    packages=['openedx_rocketchat'],
    zip_safe=False,
    entry_points={
        'lms.djangoapp': [
            'openedx_rocketchat = openedx_rocketchat.apps:OpenEdxRocketChatExtensionConfig',
        ],
        'openedx.course_tab': [
            'rocketchat = openedx_rocketchat.tabs:RocketChatTab',
        ],
    },
    install_requires=[
        'rocketchat_API==0.6.34',
        'edx-opaque-keys==0.4.4'
    ],
)
