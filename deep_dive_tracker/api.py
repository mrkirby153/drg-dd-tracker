from typing import Optional

import requests

from deep_dive_tracker.constants import DEEP_DIVE_URL
from deep_dive_tracker.deep_dive import DeepDiveSet


def get_current_deep_dives() -> Optional[DeepDiveSet]:
    resp = requests.get(DEEP_DIVE_URL)

    if resp.status_code != 200:
        return None

    return DeepDiveSet.from_api_response(resp.json())
