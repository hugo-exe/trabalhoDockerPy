FROM python:3.9-slim

WORKDIR /app

COPY requeriments.txt .

RUN pip install -r requeriments.txt

COPY . .

EXPOSE 5001

CMD ["python", "app.py"]
