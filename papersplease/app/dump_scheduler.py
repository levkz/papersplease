from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from papersplease.app.dump_manager import DumpManager
from papersplease.app.common import DataSourceEnum

app = Flask(__name__)


dump_managers = {
    DataSourceEnum.BIORXIV: DumpManager(DataSourceEnum.BIORXIV),
    DataSourceEnum.CHEMRXIV: DumpManager(DataSourceEnum.CHEMRXIV),
    DataSourceEnum.MEDRXIV: DumpManager(DataSourceEnum.MEDRXIV),
}

_syncing_in_progress = False
def is_syncing(): return _syncing_in_progress

def sync_dumps():
    global _syncing_in_progress
    _syncing_in_progress = True
    for source in dump_managers:
        dump_manager = dump_managers[source]
        dump_manager.sync()
    _syncing_in_progress = False


def init_scheduler(app: Flask):
    # Initialize and configure APScheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=sync_dumps, trigger=CronTrigger(hour=2, minute=0))  # Runs daily at midnight
    scheduler.start()

    # Ensure that the scheduler shuts down when the app stops
    with app.app_context():
        if not scheduler.running:
            scheduler.start()

    return scheduler