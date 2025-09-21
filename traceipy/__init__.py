import contextvars
from collections import defaultdict

from rich import print as rich_print
from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from sortedcontainers.sorteddict import SortedDict

from traceipy.models.stats_models import AsyncStatsInfo, InMemoryStatsDB, SyncStatsInfo


class Traceipy:
    parent_function = contextvars.ContextVar("ParentFunction", default="Init")
    parent_function_id = contextvars.ContextVar("ParentFunctionId", default="0")
    child_counter = contextvars.ContextVar("ChildCounter", default=defaultdict(int))
    call_depth = contextvars.ContextVar("CallDepth", default=0)
    call_stack = contextvars.ContextVar("CallStack", default=[])
    call_id_stack = contextvars.ContextVar("CallIdStack", default=[])

    def __init__(self):
        self.in_memory_db = InMemoryStatsDB(
            stats_dict=dict(),
            total_cpu_time=0.0,
            total_wait_time=0.0,
            trace_tree=SortedDict(),
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
        table = Table(title="Profiler Results")
        table.add_column("Parent ID", style="magenta")
        table.add_column("Parent Name", style="red")
        table.add_column("Function ID", style="cyan")
        table.add_column("Function Name", style="green")
        table.add_column("CPU Time (s)", justify="right")
        table.add_column("Wait Time (s)", justify="right")

        for function_id, function_info in self.in_memory_db.stats_dict.items():
            function_name = function_info.function_name
            parent_function_name = function_info.parent_function_name
            wait_time = 0
            if isinstance(function_info, SyncStatsInfo):
                function_name += "(SYNC)"
            else:
                wait_time = function_info.wait_time
                function_name += "(ASYNC)"

            if (
                isinstance(
                    self.in_memory_db.stats_dict.get(
                        function_info.parent_function_id, None
                    ),
                    SyncStatsInfo,
                )
                or self.in_memory_db.stats_dict.get(
                    function_info.parent_function_id, None
                )
                is None
            ):
                parent_function_name += "(SYNC)"
            else:
                parent_function_name += "(ASYNC)"

            table.add_row(
                function_info.parent_function_id,
                parent_function_name,
                function_id,
                function_name,
                f"{function_info.cpu_time:.6f}",
                f"{wait_time:.6f}",
            )
        rich_print(table)

    def construct_tree(self):
        for function_id, function_info in self.in_memory_db.stats_dict.items():
            if function_info.parent_function_id not in self.in_memory_db.trace_tree:
                self.in_memory_db.trace_tree[function_info.parent_function_id] = []
            self.in_memory_db.trace_tree[function_info.parent_function_id].append(
                function_info
            )
        for function_id, function_info in self.in_memory_db.stats_dict.items():
            self.in_memory_db.trace_tree[function_info.parent_function_id].sort()

    def construct_rich_tree(self, current_id: str, parent: Tree | None = None):
        tree = None
        if current_id != "0":
            stats = self.in_memory_db.stats_dict[current_id]

            wait_time = stats.wait_time if isinstance(stats, AsyncStatsInfo) else 0
            label = f"{stats.function_name} [CPUTime={stats.cpu_time}][WaitTime={wait_time}]"
            tree = Tree(label) if parent is None else parent.add(label)
        else:
            tree = Tree("Init Node")
        for child in self.in_memory_db.trace_tree.get(current_id, []):
            self.construct_rich_tree(current_id=child.function_id, parent=tree)
        return tree

    def display_trace_Tree(self):
        self.in_memory_db.trace_tree.clear()
        self.construct_tree()
        console = Console()
        console.print(self.construct_rich_tree("0", None))
