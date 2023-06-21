import enum
import json
from datetime import datetime
from typing import List


class DeepDiveType(enum.Enum):
    NORMAL = 1
    ELITE = 2

    @staticmethod
    def friendly_name(dd_type: "DeepDiveType") -> str:
        if dd_type == DeepDiveType.NORMAL:
            return "Deep Dive"
        elif dd_type == DeepDiveType.ELITE:
            return "Elite Deep Dive"
        else:
            raise ValueError(f"Unknown Deep Dive type: {dd_type}")


class DeepDiveSet:
    @staticmethod
    def from_api_response(response: dict) -> "DeepDiveSet":
        start_time = datetime.fromisoformat(response["startTime"])
        end_time = datetime.fromisoformat(response["endTime"])
        variants = [
            DeepDive.from_api_response(variant) for variant in response["variants"]
        ]

        return DeepDiveSet(start_time=start_time, end_time=end_time, variants=variants)

    def __init__(
        self, *, start_time: datetime, end_time: datetime, variants: List["DeepDive"]
    ):
        self.start_time = start_time
        self.end_time = end_time
        self.variants = variants

    def __repr__(self) -> str:
        return str(self.__dict__)


class DeepDive:
    @staticmethod
    def from_api_response(response: dict) -> "DeepDive":
        dd_type = response["type"]
        if dd_type == "Elite Deep Dive":
            dd_type = DeepDiveType.ELITE
        elif dd_type == "Deep Dive":
            dd_type = DeepDiveType.NORMAL
        else:
            raise ValueError(f"Unknown Deep Dive type: {dd_type}")

        return DeepDive(
            type=dd_type,
            name=response["name"],
            biome=response["biome"],
            seed=response["seed"],
            stages=[
                DeepDiveStage.from_api_response(stage) for stage in response["stages"]
            ],
        )

    def __init__(
        self,
        *,
        type: DeepDiveType,
        name: str,
        biome: str,
        seed: int,
        stages: List["DeepDiveStage"],
    ) -> None:
        self.type = type
        self.name = name
        self.biome = biome
        self.seed = seed
        self.stages = stages

    def __repr__(self) -> str:
        return str(self.__dict__)

    def get_type(self) -> str:
        return DeepDiveType.friendly_name(self.type)


class DeepDiveStage:
    @staticmethod
    def from_api_response(response: dict) -> "DeepDiveStage":
        return DeepDiveStage(
            id=response["id"],
            primary=response["primary"],
            secondary=response["secondary"],
            anomaly=response["anomaly"],
            warning=response["warning"],
        )

    def __init__(
        self, *, id: int, primary: str, secondary: str, anomaly: str, warning: str
    ):
        self.id = id
        self.primary = primary
        self.secondary = secondary
        self.anomaly = anomaly
        self.warning = warning

    def __repr__(self) -> str:
        return str(self.__dict__)
