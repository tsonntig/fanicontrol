'''
Created on 15.05.2016

@author: thomas
'''
from _collections import deque
import logging

from res.Fan_algo import use_algo


class Fan(object):
    """A sensor for the pwm class

    Attributes:
        pwm:
        sensor_path:
        target_temp:
    """
# public Functions
#
#

    def enable(self):
        with open(self.pwm_enable, "w") as pwm_file:
            pwm_file.write("1")
        with open(self.pwm_enable, "rb") as pwm_file:
            val = int(pwm_file.read())
        if val == 0:
            raise ValueError("PWM enable Value: " + str(val))

    def disable(self):
        with open(self.pwm_enable, "w") as pwm_file:
            pwm_file.write("0")
        with open(self.pwm_enable, "rb") as pwm_file:
            val = int(pwm_file.read())
        if val == 1:
            raise ValueError("PWM enable Value: " + str(val))

    def check_fan(self):
        #  no change if we changed in the last interval
        if self.alock > 0:
            self.alock = self.alock - 1
            self.logger.info(self.name + ' | Fan is locked')
            return
        correction = self._get_sensor_correction()

        #  now we can calculate the needed pwm value
        value = self.lastvalue + correction
        #  many Fans work only above a individual pwm value
        if correction > 0 and value < self.startPWM:
            value = self.startPWM
        #  minimum Speed ?
        if value < self.minPWM:
            value = self.minPWM
        #  Outside the limits ?
        elif value > 255:
            value = 255
        elif value < 0:
            value = 0
        self.pwm_history.append(value)
        # sleep is recommend ?
        if (self._all_same(self.pwm_history)):
            self.sleep = True
            return
        else:
            self.sleep = False  # no sleep recommend
        self._write_to_sys(value)
# private Functions
#
#

    def __init__(self, name, sensors_list, pwm_path, minPWM, startPWM,
                 lock, pwm_enable, algo):
        self.sensors_list = sensors_list
        # this is outside limits so we force the fan to write a new value
        self.lastvalue = -100
        self.pwm_enable = pwm_enable
        self.pwm_path = pwm_path
        self.name = name
        self.minPWM = int(minPWM)
        self.startPWM = int(startPWM)
        self.sleep = False
        self.lock = int(lock)
        self.alock = 0
        self.pwm_history = deque('9876543210', 10)
        self.logger = logging.getLogger("fanicontrol")
        self.algo = algo

    def _all_same(self, items):
        return all(x == items[0] for x in items)

    def _get_sensor_correction(self):
        #  find the sensor with the highest temperature varition
        get_temp_varition = -255
        for sensor in self.sensors_list:
            new_temp_varition = sensor.get_temp_varition()
            if new_temp_varition > get_temp_varition:
                get_temp_varition = new_temp_varition
                sensor_high = sensor.get_name()
        self.logger.info(
            self.name + ' | Highest sensor : ' + str(sensor_high))
        self.logger.debug(
            self.name + ' | Correction before multiply: ' + str(get_temp_varition))
        correction = use_algo(self, get_temp_varition,
                              self.algo, self.lastvalue)
        self.logger.debug(
            self.name + ' | Correction after multiply: ' + str(get_temp_varition))
        return correction

    def _write_to_sys(self, value):
        #  only write data if needed
        if value != self.lastvalue:
            self.logger.info(self.name + ' | Set new PWM : ' + str(value))
            with open(self.pwm_path, "w") as pwm_file:
                pwm_file.write(str(value))
            self.lastvalue = value
            self.alock = self.lock
        else:
            self.alock = self.lock
            self.logger.info(
                self.name + ' | No need to set new PWM :    ' + str(value))
