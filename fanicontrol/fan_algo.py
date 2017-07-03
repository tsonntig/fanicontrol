'''
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; version 2
 * of the License.

@author: tsonntig
'''


from _collections import deque


def use_algo(self, get_temp_varition, algo, lastvalue):
    correction = 255
    if algo == "nothing":
        correction = get_temp_varition
    elif algo == "test":
        try:
            self.pwmlist.append(lastvalue)
        except NameError:
            self.pwmlist = deque('0', 10)
            self.pwmlist.append(lastvalue)

    elif algo == "default":
        if get_temp_varition == 0:
            correction = 0
        elif get_temp_varition > 0:
            if get_temp_varition <= 1:
                correction = 1
            elif get_temp_varition <= 2:
                correction = 8
            elif get_temp_varition <= 4:
                correction = 16
            elif get_temp_varition <= 8:
                correction = 32
            elif get_temp_varition <= 10:
                correction = 64
            else:
                correction = 200
        elif get_temp_varition < 0:
            if get_temp_varition >= -1:
                correction = -1
            elif get_temp_varition >= -2:
                correction = -8
            elif get_temp_varition >= -4:
                correction = -16
            elif get_temp_varition >= -8:
                correction = -32
            elif get_temp_varition >= -10:
                correction = -64
            else:
                correction = -200
    elif algo == "aggressive":
        if get_temp_varition == 0:
            correction = 0
        elif get_temp_varition > 0:
            if get_temp_varition <= 1:
                correction = 1
            elif get_temp_varition <= 2:
                correction = 10
            elif get_temp_varition <= 3:
                correction = 30
            elif get_temp_varition <= 4:
                correction = 60
            else:
                correction = 250
        elif get_temp_varition < 0:
            if get_temp_varition >= -1:
                correction = -1
            elif get_temp_varition >= -2:
                correction = -10
            elif get_temp_varition >= -3:
                correction = -30
            elif get_temp_varition >= -4:
                correction = -60
            else:
                correction = -250

    # more tolerance (+-1) as aggressive
    elif algo == "aggressive2":
        if get_temp_varition == 0:
            correction = 0
        elif get_temp_varition > 0:
            if get_temp_varition <= 1:
                correction = 0
            elif get_temp_varition <= 2:
                correction = 1
            elif get_temp_varition <= 3:
                correction = 30
            elif get_temp_varition <= 4:
                correction = 60
            else:
                correction = 250
        elif get_temp_varition < 0:
            if get_temp_varition >= -1:
                correction = 0
            elif get_temp_varition >= -2:
                correction = -1
            elif get_temp_varition >= -3:
                correction = -30
            elif get_temp_varition >= -4:
                correction = -60
            else:
                correction = -250
    # more tolerance (+-1) as aggressive
    elif algo == "experimental":
        try:
            self.correction_list.append(get_temp_varition)
        except NameError:
            self.correction_list = deque('9999999999', 10)
        # Average except last one
        for ind, s in enumerate(self.correction_list):
            if ind == 0:
                avg = int(s)
            elif ind != 9:
                avg = avg + int(s)
        avg = avg / 9
        if get_temp_varition > (avg + 1) or get_temp_varition < (avg - 1):
            correction = get_temp_varition * 2
#####
# Do not delete this ...
#####
    else:
        raise NameError(
            '\n Config says in Fan section algo = ' + algo
            + ' \n There is no such a algo in this Version \n '
            + 'please check your config file')
    return correction
