import contextvars
import itertools

from traceipy.models.stats_models import AsyncStatsInfo, InMemoryStatsDB, SyncStatsInfo


class Traceipy:
    parent_function = contextvars.ContextVar("ParentFunction", default="Init")
    parent_function_id = contextvars.ContextVar("ParentFunctionId", default="#Init")
    call_depth = contextvars.ContextVar("CallDepth", default=0)
    call_stack = contextvars.ContextVar("CallStack", default=[])
    call_id_stack = contextvars.ContextVar("CallIdStack", default=[])

    def __init__(self):
        self.in_memory_db = InMemoryStatsDB(
            stats_dict=dict(), total_cpu_time=0.0, total_wait_time=0.0
        )

    def update_stats(
        self,
        wait_time: float,
        cpu_time: float,
        function_id: str,
        function_name: str,
        parent_function_id: str,
        parent_function_name: str,
        is_async: bool,
    ):
        if is_async:
            if self.in_memory_db.stats_dict.get(function_id, None) is None:
                self.in_memory_db.stats_dict[function_id] = AsyncStatsInfo(
                    function_name=function_name,
                    function_id=function_id,
                    parent_function_name=parent_function_name,
                    parent_function_id=parent_function_id,
                    wait_time=wait_time,
                    cpu_time=cpu_time,
                )
            else:
                self.in_memory_db.stats_dict[function_id].cpu_time += cpu_time
                self.in_memory_db.stats_dict[function_id].wait_time += wait_time  # type: ignore
        else:
            if self.in_memory_db.stats_dict.get(function_id, None) is None:
                self.in_memory_db.stats_dict[function_id] = SyncStatsInfo(
                    function_name=function_name,
                    function_id=function_id,
                    parent_function_name=parent_function_name,
                    parent_function_id=parent_function_id,
                    cpu_time=cpu_time,
                )
            else:
                self.in_memory_db.stats_dict[function_id].cpu_time += cpu_time

    def display_stats(self):
        print("_______DISPLAYING STATS_______")
        print(self.in_memory_db)
        pass
