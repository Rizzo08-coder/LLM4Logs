FROM python:3.12
WORKDIR /llm4logs
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt