class Symbol :
    def __init__(self, id: str, description: str, pip_point: float):
        self.id = id
        self.description = description
        self.pip_point = pip_point

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'description': self.description,
            'pipPoint': self.pip_point,
        }
    

