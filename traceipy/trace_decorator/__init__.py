import contextvars
import inspect
import time
from functools import wraps
from typing import Any, Callable, Coroutine

from traceipy import Traceipy


def traceipy_decorator(root_class: Traceipy):
    def parent_wrapper(
        func: Callable[..., Coroutine[Any, Any, Any]] | Callable[..., Any],
    ):
        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                current_depth = root_class.call_depth.get()
                new_depth = current_depth + 1
                root_class.call_depth.set(new_depth)

                current_function_name = func.__qualname__
                parent_function_name = root_class.parent_function.get()
                current_call_stack = root_class.call_stack.get()
                new_call_stack = current_call_stack + [func.__qualname__]

                root_class.parent_function.set(current_function_name)
                root_class.call_stack.set(new_call_stack)

                current_call_id_stack = root_class.call_id_stack.get()
                if len(current_call_id_stack) < current_depth + 1:
                    new_call_id_stack = current_call_id_stack + [1]
                else:
                    new_call_id_stack = current_call_id_stack[:current_depth] + [
                        current_call_id_stack[current_depth] + 1
                    ]

                root_class.call_id_stack.set(new_call_id_stack)
                current_call_id = (".").join(map(str, new_call_id_stack))
                parent_call_id = root_class.parent_function_id.get()
                root_class.parent_function_id.set(current_call_id)

                start_time = time.perf_counter()
                cpu_start = time.perf_counter()
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    raise e
                finally:
                    total_time = time.perf_counter() - start_time
                    total_cpu_time = time.perf_counter() - cpu_start
                    wait_time = total_time - total_cpu_time
                    root_class.update_stats(
                        wait_time=wait_time,
                        cpu_time=total_cpu_time,
                        function_id=current_call_id,
                        function_name=current_function_name,
                        parent_function_id=parent_call_id,
                        parent_function_name=parent_function_name,
                        is_async=True,
                    )
                    root_class.call_depth.set(current_depth)
                    root_class.parent_function.set(parent_function_name)
                    root_class.parent_function_id.set(parent_call_id)
                    root_class.call_id_stack.set(current_call_id_stack)
                    root_class.call_stack.set(current_call_stack)
                    if parent_function_name == "Init":
                        root_class.display_stats()

            return async_wrapper
        else:

            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                current_depth = root_class.call_depth.get()
                new_depth = current_depth + 1
                root_class.call_depth.set(new_depth)

                current_function_name = func.__qualname__
                parent_function_name = root_class.parent_function.get()
                current_call_stack = root_class.call_stack.get()
                new_call_stack = current_call_stack + [func.__qualname__]

                root_class.parent_function.set(current_function_name)
                root_class.call_stack.set(new_call_stack)

                current_call_id_stack = root_class.call_id_stack.get()
                if len(current_call_id_stack) < current_depth + 1:
                    new_call_id_stack = current_call_id_stack + [1]
                else:
                    new_call_id_stack = current_call_id_stack[:current_depth] + [
                        current_call_id_stack[current_depth] + 1
                    ]

                root_class.call_id_stack.set(new_call_id_stack)
                current_call_id = (".").join(map(str, new_call_id_stack))
                parent_call_id = root_class.parent_function_id.get()
                root_class.parent_function_id.set(current_call_id)

                start_time = time.perf_counter()
                cpu_start = time.perf_counter()
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    raise e
                finally:
                    total_time = time.perf_counter() - start_time
                    total_cpu_time = time.perf_counter() - cpu_start
                    wait_time = total_time - total_cpu_time
                    root_class.update_stats(
                        wait_time=wait_time,
                        cpu_time=total_cpu_time,
                        function_id=current_call_id,
                        function_name=current_function_name,
                        parent_function_id=parent_call_id,
                        parent_function_name=parent_function_name,
                        is_async=True,
                    )
                    root_class.call_depth.set(current_depth)
                    root_class.parent_function.set(parent_function_name)
                    root_class.parent_function_id.set(parent_call_id)
                    root_class.call_id_stack.set(current_call_id_stack)
                    root_class.call_stack.set(current_call_stack)

            return sync_wrapper

    return parent_wrapper
