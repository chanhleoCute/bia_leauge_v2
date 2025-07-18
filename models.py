# === models.py ===
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

    @staticmethod
    def from_str(label):
        label = label.strip().lower()
        if label == "sơ cấp":
            return Rank.SO_CAP
        elif label == "trung cấp":
            return Rank.TRUNG_CAP
        elif label == "cao cấp":
            return Rank.CAO_CAP
        else:
            raise ValueError(f"Không xác định được rank từ chuỗi: {label}")

class Player:
    def __init__(self, name, rank=Rank.TRUNG_CAP, total_points=0, session_points=0):
        self.name = name
        self.rank = rank
        self.total_points = total_points
        self.session_points = session_points

    def to_dict(self):
        return {
            "name": self.name,
            "rank": self.rank.value,
            "total_points": self.total_points,
            "session_points": self.session_points
        }

    @staticmethod
    def from_dict(data):
        return Player(
            data["name"],
            Rank(data["rank"]),
            data.get("total_points", 0),
            data.get("session_points", 0)
        )