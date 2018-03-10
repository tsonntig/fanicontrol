'''
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; version 2
 * of the License.

@author: tsonntig
'''

from subprocess import check_output
import logging
import re

from fanicontrol.sensor_algo import algo


class Sensor(object):
    """A sensor for the pwm class

    Attributes:
        pwm:
        sensor_path:
        target_temp:
    """

    def determine_temp_varition(self):
        self.temp = self._get_Data()
        self.correction = algo(self, self.algo, self.temp)


#  # private Functions
#  #
#  #
    def _get_Data(self):
        #  normal Sensor
        if self.sensor_normal:
            with open(self.sensor_path, "rb") as sensor_file:
                data = int(sensor_file.read(5))
                sen = float(data / 1000)  # float needed we could get an int !
        #  hddtemp sensor
        else:
            sen = check_output(["hddtemp", "-n", self.sensor_path])
        return float(sen)

    def __init__(self, name, sensor_path, target_temp, max_temp, algo):
        self.target_temp = int(target_temp)
        self.name = name
        self.sensor_path = sensor_path
        self.max_temp = int(max_temp)
        self.logger = logging.getLogger("fanicontrol")
        self.algo = algo
        if re.search("/sys/", self.sensor_path):
            self.sensor_normal = True
        elif re.search("/dev/", self.sensor_path):
            self.sensor_normal = False
        elif re.search("/proc/", self.sensor_path):
            self.sensor_normal = False
        else:
            raise ValueError("\n The Path of the sensor '"
                             + self.name
                             + " does not contain '/dev' , '/proc' or '/sys' ")
        try:
            self._get_Data()
        except:
            raise ValueError('Not a valid Path for Sensor',
                             self.name, self.sensor_path)
