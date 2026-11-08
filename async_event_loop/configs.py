import asyncio
from concurrent.futures import ThreadPoolExecutor

# Cap the background thread pool workers directly to your physical core capacity
# This guarantees that the main thread never context-switches against burst requests
MAX_COMPUTE_WORKERS = 4
thread_pool = ThreadPoolExecutor(max_workers=MAX_COMPUTE_WORKERS)
