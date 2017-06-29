#!/usr/bin/python
'''
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; version 2
 * of the License.

@author: tsonntig
'''


from setuptools import setup, find_packages
setup(
    packages=['src'],
    scripts=['src/fanicontrol', 'src/fanicontrol_autoconfig'],
)
