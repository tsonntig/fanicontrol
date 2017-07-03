#!/usr/bin/python
'''
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; version 2
 * of the License.

@author: tsonntig
'''


from setuptools import setup
setup(
    packages=['fanicontrol'],
    scripts=['fanictl', 'fanicontrol_autoconfig'],
    name="fanicontrol",
    version="0.30",
    description="fanicontrol",
    long_description="A new way to control your Fans under Linux",
    author="tsonntig",
    url="https://github.com/tsonntig/Fanicontrol",
    license="GPL2",
    platforms=["POSIX"],
)
