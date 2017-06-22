'''
Created on 15.05.2016

@author: thomas
'''
from asyncio.log import logger
from subprocess import check_output
import logging
import re

from res.Sensor_algo import algo


class Sensor(object):
    """A sensor for the pwm class

    Attributes:
        pwm:
        sensor_path:
        target_temp:
    """
#  # public Functions
#  #
#  #

    def get_algo(self):
        return self.algo

    def get_sensor_path(self):
        return self.sensor_path

    def get_maxTemp(self):
        return self.max_temp

    def get_target_temp(self):
        return self.target_temp

    def get_name(self):
        return self.name

    def get_temp_varition(self):
        return self.correction

    def get_temp(self):
        return self.temp

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
                sen = float(data / 1000)
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
