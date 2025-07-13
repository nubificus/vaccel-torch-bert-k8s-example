from prometheus_client import start_http_server, Gauge
import time
import re

DURATION_GAUGE = Gauge('vaccel_inference_duration_ms', 'Duration per inference line', ['line'])

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
    start_http_server(9100)  # Prometheus will scrape this port
    tail_log('/tmp/output.log')
