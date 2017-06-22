#!/usr/bin/python
'''
Created on 15.08.2016

@author: thomas
'''

# Try Block nedded to be sure Python is not ancient
# don't move it !!! it must be first
try:
    import sys
    import signal
    import time
    import traceback
    from res.Main_util import (
        create_fans, create_logger, create_sensors, enable_fans,
        exit_prog, get_args, get_interval, get_pinterval, list_all, log_list,
        read_config, system_check, version_check)
except Exception:
    print(
        "can't import required Modules,"
        "probably because your python is too old"
        " or some Files are missing")
    sys.exit(1)
####


def main_function():
    try:
        def signal_handler(signal, frame):
            exit_prog(fans)
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGQUIT, signal_handler)
        signal.signal(signal.SIGSEGV, signal_handler)

        version_check()
        args = get_args()
        #  the check option should be running without root or lockfile
        if args.check:
            pass
        else:
            system_check()
        config = read_config(args)
        logger = create_logger(config, args)
        sensors = create_sensors(config, logger)
        fans = create_fans(config, logger, sensors)
        #####
        # list all devices if command line option --list is given
        #####
        if args.check:
            list_all(sensors, fans)
        #####
        # check if we get all we need
        #####
        if not sensors:
            raise ValueError("No Sensor !")
        elif not fans:
            raise ValueError("No fans !")
        else:
            for fan in fans:
                if not fan.sensors_list:
                    raise ValueError(
                        "Fan " + fan.get_name() + " has no Sensor !")
        log_list(logger, fans)
        log_list(logger, sensors)
        pinterval = get_pinterval(config)
        interval = get_interval(config)
        logger.debug('Interval: ' + str(interval))
        logger.debug('P-Interval: ' + str(pinterval))
        enable_fans(fans, logger)
        main_loop(logger, fans, sensors, interval, pinterval)
    # Too avoid hardware damage we disable all Fancontrol at any Exception
    # and finally stop the program.
    except Exception as e:
        if 'logger' in locals():
            logger.exception(e)
        else:
            traceback.print_tb(e.__traceback__)
            print(e)
    finally:
        if 'fans' in locals():
            exit_prog(fans)
        else:
            exit_prog()


def main_loop(logger, fans, sensors, interval, pinterval):
    psleep = True
    logger.info('Init has been successfully finished')
    while 1:
        p = time.process_time()
        for sen in sensors:
            logger.info("Next Sensor : " + sen.get_name())
            sen.determine_temp_varition()
            logger.info('Temperature : %s', sen.get_temp())
        for fan in fans:
            logger.debug("Next Fan : " + fan.name)
            fan.check_fan()
            if not fan.sleep:
                psleep = False
        logger.debug(str(time.process_time() - p))
        if psleep:
            logger.info("Powersafemode...")
            time.sleep(int(pinterval))
        else:
            time.sleep(int(interval))
        psleep = True
####################


if __name__ == "__main__":
    main_function()
