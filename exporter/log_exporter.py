from prometheus_client import start_http_server, Summary
import time, re, os

LATENCY = Summary('vaccel_inference_latency_ms', 'Inference latency in ms')
LOG_FILE = '/tmp/output.log'

def tail_log(filepath):
    with open(filepath, 'r') as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            match = re.search(r'Line \d+: Duration: ([\d.]+) ms', line)
            if match:
                duration_ms = float(match.group(1))
                LATENCY.observe(duration_ms)

if __name__ == '__main__':
    start_http_server(9100)
    while not os.path.exists(LOG_FILE):
        time.sleep(0.5)
    tail_log(LOG_FILE)
