from functools import wraps
from fastapi import HTTPException
import time
from collections import defaultdict
import threading

class RateLimiter:
    def __init__(self):
        self.limits = defaultdict(list)
        self.lock = threading.Lock()

    def rate_limit(self, max_calls, time_frame):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                client_ip = "127.0.0.1"  # In a real app, get this from request.client.host
                current_time = time.time()

                with self.lock:
                    self.limits[client_ip] = [t for t in self.limits[client_ip] if current_time - t < time_frame]
                    if len(self.limits[client_ip]) >= max_calls:
                        raise HTTPException(status_code=429, detail=f"Rate limit exceeded: {max_calls} requests per {time_frame} seconds")
                    self.limits[client_ip].append(current_time)

                return await func(*args, **kwargs)
            return wrapper
        return decorator

rate_limiter = RateLimiter()