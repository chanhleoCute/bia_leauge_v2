from enum import Enum

class Rank(Enum):
    SO_CAP = 0
    TRUNG_CAP = 1
    CAO_CAP = 2

    def up(self):
        return Rank(min(self.value + 1, 2))

    def down(self):
        return Rank(max(self.value - 1, 0))

    def __str__(self):
        return ["Sơ cấp", "Trung cấp", "Cao cấp"][self.value]

class Player:
    def __init__(self, name, rank=Rank.TRUNG_CAP, points=0):
        self.name = name
        self.rank = rank
        self.points = points

    def to_dict(self):
        return {
            "name": self.name,
            "rank": self.rank.value,
            "points": self.points
        }

    @staticmethod
    def from_dict(data):
        return Player(data["name"], Rank(data["rank"]), data["points"])
