class Timeframe:
    def __init__(self, id, description: str, time_in_seconds: int = 0):
        self.id = id
        self.description = description
        self.interval = time_in_seconds

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'description': self.description,
            'interval': self.interval
        }

   