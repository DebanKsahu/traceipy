from dataclasses import dataclass
from functools import total_ordering
from typing import Dict, List


@total_ordering
@dataclass
class BaseStatsInfo:
    function_id: str
    function_name: str
    parent_function_id: str
    parent_function_name: str

    @staticmethod
    def parse_function_id(function_id: str):
        return tuple(int(x) for x in function_id.split("."))

    def __lt__(self, other) -> bool:
        if not hasattr(other, "function_id"):
            return NotImplemented
        return BaseStatsInfo.parse_function_id(
            self.function_id
        ) < BaseStatsInfo.parse_function_id(other.function_id)

    def __eq__(self, other) -> bool:
        if not hasattr(other, "function_id"):
            return NotImplemented
        return self.function_id == other.function_id


@dataclass
class AsyncStatsInfo(BaseStatsInfo):
    wait_time: float
    cpu_time: float


@dataclass
class SyncStatsInfo(BaseStatsInfo):
    cpu_time: float


@dataclass
class InMemoryStatsDB:
    stats_dict: Dict[str, AsyncStatsInfo | SyncStatsInfo]
    trace_tree: Dict[str, List[AsyncStatsInfo | SyncStatsInfo]]
    total_cpu_time: float
    total_wait_time: float
