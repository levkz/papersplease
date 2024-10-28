import json
import pathlib
from dateutil import parser
from datetime import datetime

CONFIG_PATH = pathlib.Path(__file__).parent.joinpath("sync_config")

def _get_source_config_path(source: str):
    return CONFIG_PATH.joinpath(f"{source}.json")

class SyncConfig:
    def __init__(self, source: str):
        self.source = source
        self.config_path = _get_source_config_path(source=source)

        data = self._read_saved_config()
        if not (data is None): self._sync_with_dict(data=data)


    def _read_saved_config(self):
        if (not self.config_path.exists()):
            self.config_path.touch()
            return None
        with open(self.config_path.resolve(), "r") as fp:
            data = json.loads(fp.read())
        return data
    
    def _save_config(self):
        if (not self.config_path.exists()):
            self.config_path.touch()
        with open(self.config_path.resolve(), "w") as fp:
            fp.write(json.dumps(self._to_dict()))


    def _to_dict(self):
        return {
            'last_synced': self.last_synced.isoformat()
        }
    
    def _sync_with_dict(self, data: dict):
        last_synced = data.get('last_synced', None)
        if (last_synced is None): return

        self.last_synced = parser.parse(last_synced)

    def update_last_synced(self, new_date: datetime):
        self.last_synced = new_date

        self._save_config()
