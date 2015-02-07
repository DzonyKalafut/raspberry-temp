import logging
import ConfigParser
from database import Sensor

__author__ = 'Jan Hajnar'
__date__ = '19.7.2014'
__license__ = 'GPL'

logger = logging.getLogger(__name__)


class AppConfig(object):
    def __init__(self):
        self.port = None
        self.temp_sensors = {}
        self.check_period = None

    def load_config(self, path):
        config_parser = ConfigParser.RawConfigParser()
        config_parser.read(path)
        try:
            self.port = config_parser.getint("webapp", "port")
            temp_sensors = config_parser.get("sensors", "temp_sensors")
            for temp_sensor in temp_sensors.split("\n"):
                sensor_parameters = temp_sensor.split(",")
                self.temp_sensors[sensor_parameters[0]] = Sensor(sensor_parameters[0],
                sensor_parameters[1], sensor_parameters[2])
            self.check_period = config_parser.getint("sensors", "check_period_mins")
        except ConfigParser.Error:
            logger.exception("Error occurred during parsing of configuration file")
