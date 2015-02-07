import threading
from flask import logging

from database import *


__author__ = 'Jan Hajnar'
__date__ = '19.7.2014'
__license__ = 'GPL'

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

class TempCheckThread(threading.Thread):
    def __init__(self, caller, sensor, period):
        threading.Thread.__init__(self);
        self.event = threading.Event()
        self.sensor = sensor
        self.period = period
        self.caller = caller

    def run(self):
        while not self.event.is_set():
            self.caller.check_temp(self.sensor)
            self.event.wait(self.period * 60)

    def stop(self):
        self.event.set()

class TempChecker(object):
    def __init__(self):
        self.checker_threads = []

    def check_temp(self, sensor):
        try:
            with open(sensor.path, "r") as sensor_file:
                lines = sensor_file.readlines()
                temperature_value = lines[1][(lines[1].index("=") + 1):]
                temperature = Temperature(sensor.id, float(temperature_value) / 1000)
                put_in_db(temperature)
        except IOError:
            logger.exception("There was an exception when trying to read sensor file '" + sensor.path + "'.")

    def check_temp_periodically(self, sensor, period):
        thread = TempCheckThread(self, sensor, period)
        thread.start()
        self.checker_threads.append(thread)

    def stop_all_checker_threads(self):
        for checker_thread in self.checker_threads:
            checker_thread.stop()
