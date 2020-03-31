'''
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; version 2
 * of the License.

@author: tsonntig
'''

from _collections import deque
import logging
from fanicontrol.fan_algo import use_algo


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

    def enable(self) -> bool:
        with open(self.pwm_enable, "w+") as pwm_file:
            self.oldpwm = pwm_file.readline().rstrip('\n')  # for restoring the fan
            pwm_file.write("1")
        check = self.check_enabled()
        if check:
            self.logger.info(self.name + " enabled")
        return check

    def check_enabled(self) -> bool:
        with open(self.pwm_enable, "r") as pwm_file:
            val = pwm_file.readline().rstrip('\n')
        return bool(val)

    def disable(self):
        with open(self.pwm_enable, "w+") as pwm_file:
            pwm_file.write(self.oldpwm)
        with open(self.pwm_enable, "r") as pwm_file:
            val = pwm_file.readline().rstrip('\n')
        if val != self.oldpwm:
            raise ValueError("PWM enable could not be restored\t" + val + " != " + self.oldpwm)      

    def sleep(self) -> bool:
        # sleep is recommend ?
        return self._all_same(self.pwm_history)

    def _all_same(self, items):
        return all(x == items[0] for x in items)

    def check_fan(self):
        correction = self._get_sensor_correction()
        # special number to indicate max Temp was reached
        if (correction == 999):
            self.pwm_history.append(255)
            self._write_to_sys(255)

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
        value = self.maxPWM if value > self.maxPWM else value
        self.pwm_history.append(value)
        self._write_to_sys(value)
# private Functions
#
#

    def __init__(self, name, sensors_list, pwm_path, minPWM, startPWM,
                 pwm_enable, algo, maxPWM):
        self.sensors_list = sensors_list
        # this is outside limits so we force the fan to write a new value
        self.lastvalue = -100
        self.pwm_enable = pwm_enable
        self.pwm_path = pwm_path
        self.name = name
        self.minPWM = int(minPWM)
        self.startPWM = int(startPWM)
        self.logger = logging.getLogger("fanicontrol")
        self.algo = algo
        self.maxPWM = int(maxPWM)
        self.pwm_history = deque('9876543210', 10)

    def _get_sensor_correction(self):
        #  find the sensor with the highest temperature varition
        get_temp_varition = -255
        for sensor in self.sensors_list:
            new_temp_varition = sensor.correction
            if new_temp_varition > get_temp_varition:
                get_temp_varition = new_temp_varition
                sensor_high = sensor.name
        self.logger.info(
            self.name + ' | Highest sensor : ' + str(sensor_high))
        if (get_temp_varition == 999):
            return 999
        self.logger.debug(
            self.name
            + ' | Correction before algo: '
            + str(get_temp_varition))
        correction = use_algo(self, get_temp_varition,
                              self.algo, self.lastvalue)
        self.logger.debug(
            self.name
            + ' | Correction after algo: '
            + str(correction))
        return correction

    def _write_to_sys(self, value):
        fan_enabled = self.check_enabled()
        if not(fan_enabled):
            self.logger.info(self.name + "not enabled")
            self.enable()
        self.logger.info(self.name + ' | Set new PWM : ' + str(value))
        with open(self.pwm_path, "w") as pwm_file:
            pwm_file.write(str(value).rstrip('\n'))
            self.lastvalue = value
