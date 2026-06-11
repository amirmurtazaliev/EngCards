FROM python:3.11-slim

WORKDIR /notifyservice

RUN apt-get update

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7070

CMD ["python", "run.py"]