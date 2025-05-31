from datetime import datetime
from typing import List, Optional
from models import  Position, Symbol  
from typing import Literal


class Session:
    def __init__(self):
        self._positions: List[Position] = []
        self._balance_history = []
        self._current_balance = 0
        self._journal_log = []

    def add_position(self, symbol:Symbol, position_type: Literal['buy', 'sell'], start_at: datetime, 
                     price: float, m_lots:int = 1, closed_at=None, close_price=None) -> Position:
        position = Position(
            id=len(self._positions) + 1,
            symbol=symbol,
            type=position_type,
            start_at=start_at,
            price=price,
            lots=m_lots / 10,
            closed_at=closed_at,
            close_price=close_price
        )
        self._positions.append(position)
        if position.get_staus() == "closed":
            self._update_balance(position)
        return position

    def get_position(self, id: int) -> Optional[dict]:
        for position in self._positions:
            if position["id"] == id:
                return position
        return None

    def close_position(self, id: int, closed_at: datetime, close_price: float):
        position = self._positions[id - 1]
        if position.get_staus() == "closed":
            return
        profit = self._get_position_profit(
        symbol=position.symbol,
        open_price=position.price, 
        close_price=close_price, 
        lots=position.lots,
        _type=  position.type)
        position.close(closed_at=closed_at, close_price=close_price, profit=profit)
        self._update_balance(closed_position=position, profit=profit)
        return position


    def get_all_positions_as_list(self) -> List[dict]:
        return self._positions.copy()
 

    def get_stats(self):
        total_profit = 0
        total_gain = 0
        total_loss = 0
        highest_profit = float('-inf')
        highest_loss = float('inf')
        consecutive_profit = 0
        consecutive_loss = 0
        highest_consecutive_profit = 0
        highest_consecutive_loss = 0

        for pos in self._positions:
            if pos.closed_at:
                profit = self._get_position_profit(pos.symbol, pos.price, pos.close_price, pos.lots, pos.type)
                total_profit += profit

                if profit > 0:
                    total_gain += profit
                    consecutive_profit += 1
                    consecutive_loss = 0
                    highest_consecutive_profit = max(highest_consecutive_profit, consecutive_profit)
                else:
                    total_loss += profit
                    consecutive_loss += 1
                    consecutive_profit = 0
                    highest_consecutive_loss = max(highest_consecutive_loss, consecutive_loss)

                highest_profit = max(highest_profit, profit)
                highest_loss = min(highest_loss, profit)

        gain_loss_ratio = total_gain / abs(total_loss) if total_loss != 0 else float('inf')

        return {
            "totalProfit": round(total_profit, 2),
            "totalGain": round(total_gain, 2),
            "totalLoss": round(total_loss, 2),
            "totalTrades": len(self._positions),
            "gainLossRatio": round(gain_loss_ratio, 2),
            "highestProfit": highest_profit,
            "highestLoss": highest_loss,
            "highestConsecutiveProfit": highest_consecutive_profit,
            "highestConsecutiveLoss": highest_consecutive_loss 
        }

    def get_chart_data(self) -> List[dict]:
        return self._balance_history.copy()
    
    def get_journal_log(self) -> List[dict]:
        return self._journal_log.copy()
    
    def log(self, message: str, level:str = 'info', date:datetime = datetime.now) -> None:
        self._journal_log.append({
            "date": date,
            "level": level,
            "message": message
        })

    
    def _update_balance(self, closed_position: Position, profit: float) -> None:
        closed_at = closed_position.closed_at
        self._current_balance += profit
        self._balance_history.append({
            "date": closed_at,
            "balance": self._current_balance
        })

    def _get_position_profit(self, symbol, open_price, close_price, lots, _type) -> float:
          pip_point = symbol.pip_point
          pips_gain = (close_price - open_price) / pip_point if _type == 'buy' else (open_price - close_price) / pip_point
          return round(pips_gain * lots, 2)


