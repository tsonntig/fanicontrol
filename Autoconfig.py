#!/usr/bin/python
'''
Created on 15.08.2016

@author: thomas
'''

# Try Block nedded to be sure Python is not acient
# don't move it !!! it must be first
try:
    import sys
    import argparse
    import os
    import re
    import traceback
    from res.Main_util import version_check
except Exception:
    print(
        "can't import, probably because your python is too old"
        " or some Files are missing")
    sys.exit(1)
####
####
####


class fano (object):

    def __init__(self, root):
        self.root = root


def get_fans(namelist):
    data = ''
    print('Search for Fans')
    fans = []
    for root, _tmp, files in os.walk('/sys'):
        f = fano(root)
        for file in files:
            if re.fullmatch('(name)', file):
                with open((root + "/" + file), "r") as name_file:
                    f.name = (name_file.readline().rstrip('\n'))
            elif re.fullmatch('(pwm[0-9]{1,2}_enable)', file):
                f.enable_file = file
            elif re.fullmatch('(pwm[0-9]{1,2})', file):
                f.pwm_file = file
        if hasattr(f, 'enable_file'):
            fans.append(f)
    for fan in fans:
        data = (
            data +
            '\n[fan_' + str(fan.name) + ']\n'
            + 'pwm_path = ' + str(fan.root) + '/' + str(fan.pwm_file) + '\n'
            + 'pwm_enable = ' + str(fan.root) + '/' + str(fan.enable_file)
            + '\n')
        sen_string = ''
        i = 0
        for name in namelist:
            sen_string = (sen_string + 'sensor_'
                          + str(i) + '_' + str(name) + ',')
            i += 1
        data = data + 'sensor_list = ' + sen_string + '\n'
        data = (data
                + 'minPWM = 30\n'
                + 'startPWM = 30\n'
                + 'algo = default\n'
                + 'lock = 5\n'
                + 'method=absolute')
    return data


def get_sensors():
    namelist = []
    data = ''
    unique_number = 0
    print('Search for Sensors')
    header_written = False
    name = ''
    for root, _tmp, files in os.walk('/sys'):
        for file in files:
            if re.fullmatch('(name)', file):
                with open((root + "/" + file), "r") as name_file:
                    name = name_file.readline().rstrip(
                        '\n')
                for file in files:
                    if re.search('(temp.*input.*)', file):
                        if not header_written:
                            data = data + \
                                '\n[sensor_' + \
                                str(unique_number) + "_" + name + ']'
                            header_written = True
                        data = (
                            data
                            + '\n'
                            + 'sensor_path = '
                            + root + '/'
                            + file)
                    if header_written:
                        data = (data
                                + '\ntarget_temp = 40\n'
                                + 'max_temp = 50\n'
                                + 'algo = default\n'
                                + 'method=absolute')
                        unique_number += 1
                        namelist.append(name)
                        header_written = False
    return data + '\n\n', namelist


def get_global():
    return(
        '#\t !Please check this file !\n'
        + '#\t try fanicontrol with the "--check" Option\n\n'
        + '[global]\n'
        + '# The measurement and Control Interval in Seconds\n'
        + 'interval = 1\n'
        + '# The Powersave Interval in Seconds\n'
        + 'pinterval = 5\n'
        + '# The Path to the Logfile\n'
        + 'logpath = /tmp/fanilog\n'
        + '# How many Infos should be in the Logfile ? \n'
        + '# Level : CRITICAL,ERROR,WARNING,INFO,DEBUG\n'
        + 'file_loglevel = DEBUG\n'
        + '# How many Infos should be to stdout ? \n'
        + '# This Value is ignored if fanicontrol is started in Daemon mode\n'
        + '# Level : CRITICAL,ERROR,WARNING,INFO,DEBUG\n'
        + 'cli_loglevel = INFO\n'
        + 'rotateLog = h\n')


def main_function():
    try:
        print(sys.version_info)
        print('Start Autoconfig, please check the generated Configfile !')
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', '--config', help='Path to configfile')
        args = parser.parse_args()
        if args.config:
            config_path = args.config
        else:
            config_path = os.getcwd() + '/fanicontrol.conf'
        print('Writing to :' + config_path)
        data_sensor, namelist = get_sensors()
        data_fans = get_fans(namelist)
        data_global = get_global()
        with open(config_path, 'w') as config_file:
            config_file.write(data_global + data_fans + data_sensor)
        print('success !\n PLease check your config with fanicontrol --check!')
    except AttributeError:
        traceback.print_exc()
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        print(e)
    sys.exit(1)


####################
if __name__ == "__main__":
    # version_check()
    main_function()
