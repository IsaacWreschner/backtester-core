from parameters import Parameters, CustomParametersDefinition
from datetime import datetime, timedelta
from typing import Callable, List, Dict, Any, Optional
from timeframe import Timeframe
from symbol import Symbol


class TestSandbox:
    def __init__(self,
                 name: str,
                 logic: Callable,
                 supported_timeframes: Dict[str, Timeframe],
                 supported_symbols: Dict[str, Symbol],
                 locked_parameters: Optional[Dict[str, bool]] = None,
                 default_parameters_values: Optional[Dict[str, Any]] = None,
                 custom_parameters_definitions: Optional[List[CustomParametersDefinition]] = None) -> None:
        self.name = name
        self.logic = logic
        self.supported_timeframes = supported_timeframes
        self.supported_symbols = supported_symbols
        self.custom_parameters_definitions = custom_parameters_definitions or []
        self._set_parameters(default_parameters_values)
        self._set_locked_parameters(locked_parameters)

    def __repr__(self) -> str:
        return (f"TestSandbox(name={self.name}, logic={self.logic.__name__}, "
                f"supported_timeframes={self.supported_timeframes}, supported_symbols={self.supported_symbols})")

        
    def metadata_to_json(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'supportedTimeframes': [Timeframe(v['id'], v['description'], v['interval']).to_json() for v in self.supported_timeframes.values()],
            'supportedSymbols': [Symbol(v['id'], v['description'], v['pip_point']).to_json() for v in self.supported_symbols.values()],
            'lockedParameters': self.locked_parameters,
            'customParametersDefinitions': [d.to_dict() for d in self.custom_parameters_definitions] ,
            'parameters': self.parameters.to_json()
        }
    
   
    def _set_locked_parameters(self, locked_parameters: Optional[Dict[str, bool]]) -> None:
        allowed_keys = {
            'start_datetime',
            'end_datetime',
            'symbol',
            'timeframe',
            'margin',
            'custom_parameters'
        }

        self.locked_parameters = {key: False for key in allowed_keys}

        if locked_parameters:
            unsupported_keys = set(locked_parameters.keys()) - allowed_keys
            if unsupported_keys:
                raise ValueError(f"Unsupported locked parameter keys: {unsupported_keys}")
            self.locked_parameters.update(locked_parameters)


    def _set_parameters(self, default_parameters_values: Optional[Dict[str, Any]]) -> None:
        # Initialize custom_parameters from definitions
        default_custom_parameters = {
            d.name: d.default_value for d in self.custom_parameters_definitions
        }

        self.parameters = Parameters(
            start_datetime=datetime.now() - timedelta(days=365),
            end_datetime=datetime.now(),
            symbol="",
            timeframe="1d",
            margin=0.5,
            custom_parameters=default_custom_parameters
        )

        if default_parameters_values:
            if 'customizedParameters' in default_parameters_values:
                raise ValueError("Do not include 'customizedParameters' in default_parameters_values. "
                                "Custom parameters are set from custom_parameters_definitions.")
            self.update_parameters(default_parameters_values)
            

    def update_parameters(self, parameters: Dict[str, Any]) -> None:
        valid_keys = {'start_datetime', 'end_datetime', 'symbol', 'timeframe', 'margin', 'custom_parameters'}
        for key in parameters:
            if key not in valid_keys:
                raise ValueError(f"Invalid parameter key: {key}")

        for key, value in parameters.items():
            if key == 'custom_parameters':
                self.update_custom_parameters(value)
            else:
                setattr(self.parameters, key, value)

    def update_custom_parameters(self, custom_parameters: Dict[str, Any]) -> None:
        valid_custom_keys = {d.name for d in self.custom_parameters_definitions}
        for key in custom_parameters:
            if key not in valid_custom_keys:
                raise ValueError(f"Invalid custom parameter key: {key}")
        self.parameters.custom_parameters.update(custom_parameters)
