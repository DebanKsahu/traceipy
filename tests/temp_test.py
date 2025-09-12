import asyncio

from traceipy import Traceipy
from traceipy.trace_decorator import traceipy_decorator

root_class = Traceipy()


@traceipy_decorator(root_class=root_class)
def cpu_bound(n):
    total = 0
    for i in range(n):
        total += i * i
    return total


@traceipy_decorator(root_class=root_class)
async def slow_async():
    await asyncio.sleep(1)
    return cpu_bound(1000000)


@traceipy_decorator(root_class=root_class)
async def main():
    x = await slow_async()
    y = cpu_bound(10000)
    return x + y


if __name__ == "__main__":
    result = asyncio.run(main())
    print("Final result:", result)
