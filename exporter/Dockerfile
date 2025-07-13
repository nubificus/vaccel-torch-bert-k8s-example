FROM python:3.11-slim
RUN pip install prometheus_client
COPY log_exporter.py /log_exporter.py
CMD ["python", "/log_exporter.py"]

