FROM python:3.9-slim

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY healthcheck.py /
COPY main.py /

ENTRYPOINT ["gunicorn", "main:app", "-w", "2", "--threads", "2", "-b 0.0.0.0:8000"]

