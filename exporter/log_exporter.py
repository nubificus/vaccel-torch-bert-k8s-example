from prometheus_client import start_http_server, Summary, Counter
import time
import re
import os

INFERENCE_LATENCY = Summary('vaccel_inference_latency_seconds',
                            'Inference latency in milliseconds')

INFERENCE_COUNTER = Counter('vaccel_inference_total',
                            'Total number of inferences')

LOG_FILE = '/tmp/output.log'

def wait_for_file(filepath):
    while not os.path.exists(filepath):
        print(f"Waiting for {filepath}...")
        time.sleep(0.5)

def tail_log(filepath):
    with open(filepath, 'r') as f:
        f.seek(0, 2)  # Go to end of file
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            match = re.search(r'Line \d+: Duration: ([\d.]+) ms', line)
            if match:
                duration_ms = float(match.group(1))
                INFERENCE_LATENCY.observe(duration_ms)
                INFERENCE_COUNTER.inc()

if __name__ == '__main__':
    start_http_server(9100)
    wait_for_file(LOG_FILE)
    tail_log(LOG_FILE)
