import concurrent.futures
import urllib.request
import time

URL = "http://127.0.0.1:9000" # Aapke server ka address
TOTAL_REQUESTS = 200          # Total kitne fire karne hain
CONCURRENCY_LIMIT = 100       # Ek sath (parallel) kitne bomb girengay

def send_request(request_id):
    try:
        start_time = time.time()
        # Raw request bhej rahe hain bina kisi external library ke
        with urllib.request.urlopen(URL, timeout=5) as response:
            html = response.read()
            latency = time.time() - start_time
            print(f"[Req {request_id}] Success! Latency: {latency:.4f}s")
    except Exception as e:
        print(f"[Req {request_id}] FAILED: {e}")

print(f"Bombing started... Sending {TOTAL_REQUESTS} requests with concurrency of {CONCURRENCY_LIMIT}")
start_bombing = time.time()

# ThreadPoolExecutor ek sath kai threads khol kar parallel requests fire karega
with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENCY_LIMIT) as executor:
    executor.map(send_request, range(TOTAL_REQUESTS))

print(f"\nBombing finished in {time.time() - start_bombing:.2f} seconds!")
