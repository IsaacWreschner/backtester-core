from typing import Dict, Any
import pandas as pd

class ResultsRequest:
    def __init__(self, parameters: Dict[str, Any]):
        if 'start_datetime' in parameters:
            parameters['start_datetime'] = self._to_utc_timestamp(parameters['start_datetime'])
        if 'end_datetime' in parameters:
            parameters['end_datetime'] = self._to_utc_timestamp(parameters['end_datetime'])

        print(f'[DEBUG] ResultsRequest: {parameters}')
        self.parameters = parameters

    @staticmethod
    def _to_utc_timestamp(value: Any) -> pd.Timestamp:
        ts = pd.Timestamp(value)
        # If it's timezone-naive, assume UTC
        if ts.tzinfo is not None:
            ts = ts.tz_localize(None)
        return ts

    @staticmethod
    def from_json(json: dict) -> 'ResultsRequest':
        print('[DEBUG] ResultsRequest.from_json')
        key_map = {
            'startDatetime': 'start_datetime',
            'endDatetime': 'end_datetime',
            'symbol': 'symbol',
            'timeframe': 'timeframe',
            'margin': 'margin',
            'customParameters': 'custom_parameters'
        }

        converted = {
            new_key: json[old_key]
            for old_key, new_key in key_map.items()
            if old_key in json
        }

        

        return ResultsRequest(parameters=converted)
