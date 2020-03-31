'''
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; version 2
 * of the License.

@author: tsonntig
'''


#  if you want to change, just write a new elif
#  and finally change the config file
from _collections import deque


def algo(self, algo, temp):
    #  hard limit hit ?
    if temp > self.max_temp:
        self.logger.warning(str(self.name) + " max Temp !!! \n")
        return 999
    #
    #
    #  if your sensor gives always correct data
    #  use this one
    #
    if (algo == 'default'):
        return int(temp - self.target_temp)

    elif (algo == '3to1'):
        try:
            self.measurements.append(temp)
        except Exception as e:
            print(e)
            self.measurements = deque('999', 3)
        #  determine the average correction
        correction = 0
        for s in self.measurements:
            correction = correction + s
        correction = correction / 3
        correction = correction - self.target_temp
        self.logger.debug(
            self.name + ' | Correction: ' +
            str(correction) + ' target Temp: ' + str(self.target_temp))
        return int(correction)
#
#
#  enhanced one for very buggy sensors
#
#
    elif (algo == 'buggysensor'):
        try:
            self.measurements.append(temp)
        except NameError:
            self.measurements = deque('9999999999', 10)
        #  determine the average correction
        correction = 0
        w = 1
        for s in self.measurements:
            if w == 10:
                correction = correction + (int(s) * 18)
            else:
                correction = correction + (int(s))
            self.logger.debug("List :" + str(s) + " | " + str(correction))
            w = w + 1
        correction = correction / 27
        self.logger.debug('avg temp :  ' + str(correction))
        correction = correction - self.target_temp
        self.logger.debug(
            self.name + ' | Correction: ' +
            str(correction) + ' target Temp: ' + str(self.target_temp))
        return int(correction)

    elif (algo == 'exsensor'):
        try:
            self.measurements.append(temp)
        except NameError:
            self.measurements = deque('0', 60)
            for _i in range(1, 60):
                self.measurements.append(temp)
        #  determine the average correction
        x = 0
        for s in self.measurements:
            x = x + int(s)
        avg = x / 60  # Average from all measurements
        cur = (self.measurements[57] +
               self.measurements[58] + self.measurements[59]) / 3
        abw = cur - self.target_temp
        diff = (cur - avg)
        self.logger.debug('TEMP :  ' + str(cur))
        self.logger.debug('AVG :  ' + str(avg))
        self.logger.debug('Diff :  ' + str(abw))

        correction = diff + abw
        self.logger.debug(
            self.name + ' | Correction: ' +
            str(correction) + ' target Temp: ' + str(self.target_temp))
        return int(correction)

#
#
#  your own ???
#
#
    elif (algo == 'own'):
        #  hard limit hit ?
        if self.measurements[9] > self.max_temp:
            self.logger.info("max Temp !!! \n ****************")
            self.correction = 255
        else:
            self.correction = int(self.measurements[9] - self.target_temp)
#####
# Do not delete this ...
#####
    else:
        raise NameError(
            '\n Config says in Sensor section algo = ' + algo
            + ' \n There is no such a algo in this Version \n '
            + 'please check your config file')
