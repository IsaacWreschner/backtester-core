from datetime import datetime
from typing import Literal
from .symbol import Symbol

class Position:
    def __init__(self, id: int, symbol:Symbol, type: Literal['buy', 'sell'], 
                 start_at: datetime, price: float, lots:float = 0.1,
                   closed_at: datetime = None, close_price: float = None,
                   profit: float = None) -> None:
        self.id = id
        self.symbol = symbol
        self.type = type
        self.start_at = start_at
        self.price = price
        self.lots = lots
        self.closed_at = closed_at
        self.close_price = close_price
        self.profit = profit
        self._status = "open"  if closed_at is None else "closed"

    def close(self, closed_at: datetime, close_price: float, 
              profit: float) -> None:
        """Closes the position."""
        self.closed_at = closed_at
        self.close_price = close_price
        self.profit = profit
        self._status = "closed"

    def get_staus(self) -> Literal['open', 'closed']:
        """Returns the status of the position."""
        return self._status
    
    def to_json(self) -> dict:
        return {
            'id': self.id,
            'symbol': self.symbol.to_json(),
            'type': self.type,
            'startedAt': self.start_at,
            'price': self.price,
            'lots': self.lots,
            'closedAt': self.closed_at if self.closed_at else None,
            'closePrice': self.close_price,
            'profit': self.profit,
        }
    
    def __repr__(self):
        return f"Position(symbol={self.symbol.id},  entry_price={self.price}, exit_price={self.close_price}, type={self.type}, status={self._status})"
    
    