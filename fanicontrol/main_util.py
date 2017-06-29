'''
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; version 2
 * of the License.

@author: tsonntig
'''


from configparser import NoOptionError
from logging.handlers import TimedRotatingFileHandler
import argparse
import configparser
import getpass
import logging
import os.path
import re
import sys

from fanicontrol.fan import Fan
from fanicontrol.sensor import Sensor


def enable_fans(fans, logger):
    for fan in fans:
        fan.enable()


def exit_prog(*args):
    try:
        os.remove("/tmp/fanictl.lk")
    except:
        if not os.path.isfile("/tmp/fanictl.lk"):
            pass
        else:
            print("Could not remove Lockfile !", file=sys.stderr)
    #  should be used for fans
    try:
        for ar in args:
            for fan in ar:
                if isinstance(fan, Fan):
                    fan.disable()
    except:
        print("Could not restore Fans !", file=sys.stderr)
    finally:
        os._exit(1)


def log_list(logger, *arg):
    logger.debug(" ".join(map(str, arg)))


def read_config(args):
    config = configparser.ConfigParser()
    if args.config:
        config.read(args.config)
        print('Config: ' + args.config)
    else:
        config.read("/etc/fanicontrol.conf")
        print('Config: ' + '/etc/fanicontrol.conf')
    if config.sections() == []:
        raise ValueError('The Configfile seems to be empty !')
    return config


def create_logger(config, args):
    try:
        #  config file
        fh_loglevel = config.get('global', 'file_loglevel')
        cli_loglevel = config.get('global', 'cli_loglevel')
        rotateLog = config.get('global', 'rotateLog')

        if args.check:
            logname = config.get('global', 'logpath') + '_check'
        else:
            logname = config.get('global', 'logpath')

    except:
        #  default
        logname = "/var/log/default_fanilog"
        fh_loglevel = "DEBUG"
        cli_loglevel = "DEBUG"
        rotateLog = "d"

    logger = logging.getLogger("fanicontrol")
    logger.setLevel(logging.DEBUG)
    if fh_loglevel == "None":
        fh = TimedRotatingFileHandler(
            logname, when=rotateLog, interval=1, backupCount=3)
        fh.setLevel(fh_loglevel)
        fmt = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(funcName)s | %(message)s',
            "%m-%d %H:%M:%S")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    if cli_loglevel == "None":
        cli = logging.StreamHandler()
        cli.setLevel(cli_loglevel)
        cli.setFormatter(fmt)
        logger.addHandler(cli)
    logger.info(sys.version)
    return logger


def _find_device(name_device):
    for root, _tmp, files in os.walk('/sys'):
        for file in files:
            if re.fullmatch('(name)', file):
                with open((root + "/" + file), "r") as name_file:
                    check_name = name_file.readline().rstrip('\n')
                if check_name == name_device:
                    path_d = root
                    break
    return path_d


def create_sensors(config, logger):
    sensors = []
    for section_name in config.sections():
        if re.search("sensor", section_name):
            try:
                method = config.get(section_name, 'method')
                if method == 'relative':
                    device_name = config.get(section_name, 'device_Name')
                    sensor_name = config.get(section_name, 'sensor_Name')
                    arg1 = _find_device(device_name) + '/' + sensor_name
                elif method == 'absolute':
                    arg1 = config.get(section_name, "sensor_path")
                else:
                    raise ValueError('Unknown method: ' + method)
            except NoOptionError:
                logger.warn("No method in Config file")
                arg1 = config.get(section_name, "sensor_path")
            arg2 = config.get(section_name, "target_temp")
            arg3 = config.get(section_name, "max_temp")
            arg4 = config.get(section_name, "algo")
            logger.debug
            ('New Sensor :' + section_name
             + ' at: ' + arg1
             + ' target Temp: ' + arg2
             + 'max temp : ' + arg3
             + 'algo :' + arg4)
            sens = Sensor(section_name, arg1, arg2, arg3, arg4)
            sensors.append(sens)
    return sensors


def create_fans(config, logger, sensors):
    fans = []
    for section_name in config.sections():
        if re.search("fan", section_name):
            newsensors = []
            try:
                method = config.get(section_name, 'method')
                if method == 'relative':
                    device_name = config.get(section_name, 'device_Name')
                    fan_name = config.get(section_name, 'fan_Name')
                    path_f = _find_device(device_name)
                    arg2 = path_f + '/' + fan_name
                    arg6 = path_f + '/' + fan_name + '_enable'
                elif method == 'absolute':
                    arg2 = config.get(section_name, "pwm_path")
                    arg6 = config.get(section_name, "pwm_enable")
                else:
                    raise ValueError('Unknown method: ' + method)
            except NoOptionError:
                logger.warn("No method in Config file")
                arg2 = config.get(section_name, "pwm_path")
                arg6 = config.get(section_name, "pwm_enable")
            arg1 = config.get(section_name, "sensor_list")
            array = arg1.split(",")
            for val in array:
                for sensor in sensors:
                    if val == sensor.name:
                        newsensors.append(sensor)
            arg3 = config.get(section_name, "minPWM")
            arg4 = config.get(section_name, "startPWM")
            arg5 = config.get(section_name, "lock")
            arg7 = config.get(section_name, "algo")
            logger.debug(
                'New Fan :' + section_name
                + ' at: ' + arg2 + arg3 + arg4 + arg5 + arg6 + arg7)
            fanv = Fan(
                section_name, newsensors, arg2, arg3, arg4, arg5, arg6, arg7)
            fans.append(fanv)
    return fans


def get_interval(config):
    try:
        interval = config.get('global', 'interval')
    except:
        interval = 1
    return interval


def get_pinterval(config):
    try:
        pinterval = config.get('global', 'pinterval')
    except:
        pinterval = 5
    return pinterval


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Path to configfile")
    parser.add_argument(
        "--check", action='store_true',
        help="check all configured fans and sensors")
    args = parser.parse_args()
    return args


def version_check():
    if (sys.version_info < (3, 5)):
        print('Your Python is too old : \n' + str(sys.version_info.major)
              + '.' + str(sys.version_info.minor)
              + '\nneeded: >= 3.5')
        sys.exit(1)


def system_check():
    #####
    # Check Root
    #####
    if (getpass.getuser() != 'root'):
        print("We can't do anything without root. User: "
              + getpass.getuser(), file=sys.stderr)
        sys.exit(1)
    #####
    # Lockfile
    #####
    if os.path.isfile("/tmp/fanictl.lk"):
        print(
            "Lockfile already exists ! Is there an other Instance running ?",
            file=sys.stderr)
        sys.exit(1)
    with open("/tmp/fanictl.lk", "w") as lock_file:
        lock_file.write("")


def list_all(sensors, fans):
    if fans:
        print("**** FANS ****")
        for fan in fans:
            print(
                "\n NAME        : " + str(fan.name)
                + "\n PWM PATH    : " + str(fan.pwm_path)
                + "\n MIN PWM     : " + str(fan.minPWM)
                + "\n START PWM   : " + str(fan.startPWM)
                + "\n ENABLE PATH : " + str(fan.pwm_enable)
            )
            print(" SENSORS: ")
            for sensor in fan.sensors_list:
                print(" \t\t" + sensor.name)
    if sensors:
        print("\n**** SENSORS ****")
        for s in sensors:
            s.determine_temp_varition()
            print(
                "\n NAME        : " + s.name
                + "\n SENSOR PATH     : " + s.sensor_path
                + "\n MAX TEMP    : " + str(s.max_temp)
                + "\n TARGET TEMP : " + str(s.target_temp)
                + "\n ALGO   : " + s.algo
                + '\n TEMERATURE VARIATION: ' +
                str(s.correction)
            )
    sys.exit(0)  # We have no lockfile or Fans to disable
