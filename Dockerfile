FROM python:3.10-slim

RUN apt-get update && apt-get install -y     chromium     chromium-driver     && apt-get clean

ENV CHROME_BIN=/usr/bin/chromium
ENV PATH=$PATH:/usr/lib/chromium/

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "script.py"]
