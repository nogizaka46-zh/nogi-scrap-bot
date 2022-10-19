from typing import Any, Awaitable, List
import asyncio


def create_event_queue(arr: List, func: Any):
    tasks = []
    for item in arr:
        tasks.append(asyncio.create_task(func(item)))


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


# async def run_parallel_with_futures(*functions: Awaitable[Any], iterables: Array) -> Any:
#     create_event_queue()
