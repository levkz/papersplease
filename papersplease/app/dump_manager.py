import pandas as pd
import pathlib
from datetime import datetime
from papersplease.app.sync_data import SyncConfig
from papersplease.app.common import DataSourceEnum

from paperscraper.get_dumps import medrxiv, biorxiv, chemrxiv

xrxiv_dump_mapping = {
    DataSourceEnum.BIORXIV: biorxiv,
    DataSourceEnum.MEDRXIV: medrxiv,
    DataSourceEnum.CHEMRXIV: chemrxiv,
}

XRXIV_DUMPS_PATH = pathlib.Path(__file__).parent.joinpath("xrxiv_dumps")

def get_xrxiv_dump_path(xrxiv_repo: str):
    return XRXIV_DUMPS_PATH.joinpath(f'{xrxiv_repo}.jsonl').resolve()

def get_xrxiv_temp_dump_path(xrxiv_repo: str):
    return XRXIV_DUMPS_PATH.joinpath(f'{xrxiv_repo}--temp.jsonl').resolve()

class DumpManager:
    def __init__(self, source: str):
        self.source = source
        self.sync_config = SyncConfig(source=source)

    def sync(self):
        last_synced = self.sync_config.last_synced
        new_sync = datetime.now()

        if (new_sync.date() == last_synced.date()): return

        source_dump_path = get_xrxiv_dump_path(self.source)
        temp_dump_path = get_xrxiv_temp_dump_path(self.source)

        xrxiv_dump_mapping[self.source](
            begin_date=last_synced.isoformat(),
            end_date=new_sync.isoformat(),
            save_path=temp_dump_path,
        )

        with source_dump_path.open('a') as to_file:
            to_file.seek(0, 2)
            if to_file.tell() > 0:
                to_file.write('\n')

            with temp_dump_path.open('r') as from_file:
                for line in from_file:
                    to_file.write(line)
        
        dataframe = pd.read_json(source_dump_path, lines=True)

        removed = dataframe.drop_duplicates(subset='doi', keep='last')
        removed['date'] = pd.to_datetime(removed['date'], errors='coerce', unit='ms')
        removed.to_json(source_dump_path, orient='records', lines=True, date_format='iso')

        self.sync_config.update_last_synced(new_date=new_sync)
