from prometheus_client import start_http_server, Gauge
import time
import re
import os

DURATION_GAUGE = Gauge('vaccel_inference_duration_ms', 'Duration per inference line', ['line'])

LOG_FILE = '/tmp/output.log'

def wait_for_file(filepath):
    while not os.path.exists(filepath):
        print(f"Waiting for {filepath}...")
        time.sleep(0.5)

def tail_log(filepath):
    with open(filepath, 'r') as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            match = re.search(r'Line (\d+): Duration: ([\d.]+) ms', line)
            if match:
                line_number = match.group(1)
                duration_ms = float(match.group(2))
                DURATION_GAUGE.labels(line=line_number).set(duration_ms)

if __name__ == '__main__':
    start_http_server(9100)
    wait_for_file(LOG_FILE)
    tail_log(LOG_FILE)

