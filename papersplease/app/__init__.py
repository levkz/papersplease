"""
Papersplease demo
"""

from flask import Flask
from papersplease.app.dump_scheduler import init_scheduler
from papersplease.app.api import paperscraper_bp
app = Flask(__name__)

#Configuration of application, see configuration.py, choose one and uncomment.
#app.config.from_object('configuration.ProductionConfig')
app.config.from_object('papersplease.app.config.DevelopmentConfig')
app.register_blueprint(paperscraper_bp)

#app.config.from_object('configuration.TestingConfig')

scheduler = init_scheduler(app=app)