import hashlib
from datetime import datetime
from time import time
import pytz

from data.config import nmt_24_126, nmt_24_172


def generate_inline_id(query: str):
    return hashlib.md5(f'{query}{time()}'.encode()).hexdigest()


def validate_datetime(value: str) -> datetime:
    try:
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        raise ValueError('Invalid date format. Use YYYY-MM-DD HH:MM:SS')


def convert_datetime_from_local_to_utc(value: datetime, timezone='Europe/Kiev') -> datetime:
    local = pytz.timezone(timezone)
    local_dt = local.localize(value, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    # reformat to YYYY-MM-DD HH:MM:SS
    return datetime.strptime(utc_dt.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')


def get_weight_of_sciences(science, speciality):
    nmt_24 = nmt_24_126 if speciality == 126 else nmt_24_172
    for value in nmt_24.values():
        if isinstance(value, dict):
            if value['subject'] == science:
                return value['weight']
        elif isinstance(value, list):
            for subject in value:
                if subject['subject'] == science:
                    return subject['weight']

