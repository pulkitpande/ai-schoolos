from fastapi import Request, Response
from typing import Callable, Awaitable

async def example_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]):
    response = await call_next(request)
    response.headers['X-Example-Middleware'] = 'Active'
    return response 