from flask.ext.sqlalchemy import SQLAlchemy
import time
import threading
from flask import logging

__author__ = 'Jan Hajnar'
__date__ = '19.7.2014'
__license__ = 'GPL'

db = SQLAlchemy()
lock = threading.RLock()

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


class Temperature(db.Model):
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    temperature = db.Column(db.Float, unique=False)
    time = db.Column(db.Integer, primary_key=True)
    sensor = db.relationship('Sensor', uselist=False)

    def __init__(self, sensor_id, temperature):
        self.sensor_id = sensor_id
        self.temperature = temperature
        self.time = int(time.time())


class Sensor(db.Model):
    id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text, unique=False)
    path = db.Column(db.Text, unique=True)


    def __init__(self, id, name, path):
        self.id = id
        self.name = name
        self.path = path


def put_in_db(object_to_put):
    with lock:
        try:
            db.session.add(object_to_put)
            db.session.commit()
        except Exception:
            logger.exception("exception")
