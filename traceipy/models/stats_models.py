from dataclasses import dataclass
from typing import Dict


@dataclass
class AsyncStatsInfo:
    function_name: str
    function_id: str
    parent_function_name: str
    parent_function_id: str
    wait_time: float
    cpu_time: float


@dataclass
class SyncStatsInfo:
    function_id: str
    function_name: str
    parent_function_id: str
    parent_function_name: str
    cpu_time: float


@dataclass
class InMemoryStatsDB:
    stats_dict: Dict[str, AsyncStatsInfo | SyncStatsInfo]
    total_cpu_time: float
    total_wait_time: float
