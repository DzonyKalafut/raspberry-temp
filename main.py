from flask import Flask, render_template
from flask.ext.restless import APIManager
from app_config import AppConfig
from database import *
from temp_checker import TempChecker
import signal
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/raspberry-temp.db?check_same_thread=False'
db.app = app
db.init_app(app)
app_config = AppConfig()
app.debug = False
db.create_all()
temp_checker = TempChecker()


def pagination_remover(result=None, **kw):
    for key in result.keys():
        if key != 'objects':
            del result[key]

manager = APIManager(app, flask_sqlalchemy_db=db, postprocessors={'GET_MANY': [pagination_remover]})
manager.create_api(Temperature, methods=['GET'], results_per_page="k")
manager.create_api(Sensor, methods=['GET'], results_per_page="-1")


@app.route("/")
def index():
    temperatures = []
    for sensor in Sensor.query.all():
        temperature = Temperature.query.filter_by(sensor_id=sensor.id).order_by(Temperature.time.desc()).first()
        if temperature is not None:
            temperatures.append(temperature)
    return render_template("index.html", data=temperatures)


def init_app():
    app_config.load_config("config/config.cfg")
    for temp_sensor in app_config.temp_sensors.values():
        db_sensor = Sensor.query.filter_by(name=temp_sensor.name).first()
        if db_sensor is None:
            put_in_db(temp_sensor)
        temp_checker.check_temp_periodically(temp_sensor, app_config.check_period)


def signal_handler(signal, frame):
    temp_checker.stop_all_checker_threads()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    init_app()
    app.run(host="0.0.0.0", port=app_config.port)
