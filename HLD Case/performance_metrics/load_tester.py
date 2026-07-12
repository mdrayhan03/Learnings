import asyncio
import time
import math
import aiohttp

# Target configurations (Ensure one of your previous servers is actively running on this port!)
TARGET_URL = "http://127.0.0.1:8081/" 
TOTAL_REQUESTS = 200
CONCURRENCY_LEVEL = 20

async def fire_single_request(session: aiohttp.ClientSession, request_id: int) -> float | None:
    """Fires a single HTTP request and measures high-resolution latency."""
    start_time = time.perf_counter()
    try:
        async with session.get(TARGET_URL) as response:
            # Force reading the response body text to complete the cycle
            await response.text()
            end_time = time.perf_counter()
            
            latency = (end_time - start_time) * 1000 # Convert to milliseconds
            return latency
    except Exception as e:
        # Network dropouts, connection drops, or timeouts
        return None

async def worker(session: aiohttp.ClientSession, queue: asyncio.Queue, results: list):
    """Worker task that continuously pulls request tasks out of the shared queue."""
    while not queue.empty():
        request_id = await queue.get()
        latency = await fire_single_request(session, request_id)
        if latency is not None:
            results.append(latency)
        queue.task_done()

async def main():
    print("=" * 60)
    print("      DISTRIBUTED SYSTEM LOAD TESTING ENGINE")
    print("=" * 60)
    print(f"Target URL:       {TARGET_URL}")
    print(f"Total Requests:   {TOTAL_REQUESTS}")
    print(f"Concurrency Goal: {CONCURRENCY_LEVEL} parallel workers")
    print("-" * 60)

    # Populate a task queue with request indices
    task_queue = asyncio.Queue()
    for i in range(1, TOTAL_REQUESTS + 1):
        task_queue.put_nowait(i)

    latencies = []
    
    # Track metrics for the entire test cycle window
    test_start_time = time.perf_counter()
    
    # Execute connections efficiently using an HTTP client session connection pool
    async with aiohttp.ClientSession() as session:
        # Spawn our concurrent worker tasks pool
        workers = [
            asyncio.create_task(worker(session, task_queue, latencies))
            for _ in range(CONCURRENCY_LEVEL)
        ]
        
        # Wait until every item in the queue has been processed completely
        await task_queue.join()
        
        # Kill idle workers
        for w in workers:
            w.cancel()

    test_end_time = time.perf_counter()
    total_elapsed_time = test_end_time - test_start_time

    # --- METRICS MATHEMATICAL CALCULATIONS TIER ---
    successful_requests = len(latencies)
    if successful_requests == 0:
        print("❌ Error: All requests failed. Is your target server online?")
        return

    # Sort array in ascending order to extract accurate percentile placements
    latencies.sort()
    
    avg_latency = sum(latencies) / successful_requests
    throughput_rps = successful_requests / total_elapsed_time
    
    # Calculate index positions for percentiles
    p95_index = math.ceil(successful_requests * 0.95) - 1
    p99_index = math.ceil(successful_requests * 0.99) - 1
    
    p95_latency = latencies[p95_index]
    p99_latency = latencies[p99_index]

    # Display final aggregated analytics report
    print("\n📊 AGGREGATED METRICS ANALYSIS REPORT:")
    print(f"  • Successful Responses Captured : {successful_requests} / {TOTAL_REQUESTS}")
    print(f"  • Total Load Time Duration      : {total_elapsed_time:.3f} seconds")
    print(f"  • Calculated Throughput         : {throughput_rps:.2f} Requests/Sec (RPS)")
    print(f"  • Average Node Latency          : {avg_latency:.2f} ms")
    print(f"  • 95th Percentile Latency (p95) : {p95_latency:.2f} ms")
    print(f"  • 99th Percentile Latency (p99) : {p99_latency:.2f} ms")
    print("=" * 60)

if __name__ == "__main__":
    # Ensure aiohttp doesn't trigger loop exceptions on windows systems
    asyncio.run(main())