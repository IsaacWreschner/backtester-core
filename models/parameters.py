from datetime import datetime
from typing import Literal

class Parameters:
  def __init__(self, start_datetime: datetime, end_datetime: datetime, symbol: str, timeframe: str, margin: float = 0.5, custom_parameters: dict = None):
    self.start_datetime = start_datetime
    self.end_datetime = end_datetime
    self.symbol = symbol
    self.timeframe = timeframe
    self.margin = margin
    self.custom_parameters = custom_parameters if custom_parameters else {}

  def __repr__(self):
    return f"Parameters(start_datetime={self.start_datetime}, end_datetime={self.end_datetime}, symbol={self.symbol}, timeframe={self.timeframe}, margin={self.margin}, custom_parameters={self.custom_parameters})"

  def to_json(self) -> dict:
    return {
      'startDatetime': self.start_datetime,
      'endDatetime': self.end_datetime,
      'symbol': self.symbol,
      'timeframe': self.timeframe,
      'margin': self.margin,
      'customParameters': self.custom_parameters
    }
  
  
    
class CustomParametersDefinition:
    def __init__(self, name: str, description: str, default_value: str, 
                 type: Literal['string', 'number', 'boolean', 'select'],
                 options: list = None) -> None:
        self.options = options if options else []
        self.name = name
        self.description = description
        self.default_value = default_value
        self.type = type

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'description': self.description,
            'defaultValue': self.default_value,
            'type': self.type,
            'options': self.options
        }

#def from_json(self, data: dict) -> None:
#    return Parameters(
#      start_datetime=data.get('startDatetime'),
#      end_datetime=data.get('endDatetime'),
#      symbol=data.get('symbol'),
#      timeframe=data.get('timeframe'),
#      margin=data.get('margin', 0.5),
#      custom_parameters=data.get('customParameters', {})
#    )