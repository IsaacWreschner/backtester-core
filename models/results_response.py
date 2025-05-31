from typing import List, Dict, Any
from position import Position
from test_sandbox import TestSandbox 

class ResultsResponse:
    def __init__(self, sandbox: TestSandbox, position_list:List[Position], stats:Dict[str, Any], 
                 balance_chart:List[Dict[str, Any]], journalLog:List[Dict[str, Any]] = None) -> None:
        self.sandbox = sandbox
        self.position_list = position_list
        self.stats = stats
        self.balance_chart = balance_chart
        self.journalLog = journalLog if journalLog else []

    def to_json(self) -> Dict[str, Any]:
        return {
            'sandbox': self.sandbox.metadata_to_json(),
            'positionsList': [position.to_json() for position in self.position_list],
            'stats': self.stats,
            'balanceChart': self.balance_chart,
            'journalLog': self.journalLog
        }
    
