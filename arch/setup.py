#!/usr/bin/python
'''
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; version 2
 * of the License.

@author: tsonntig
'''


from distutils.core import setup
setup(
    package=['src'],
    package_dir={'': 'src'},
    scripts=['fanicontrol', 'autoconfig'],
)
