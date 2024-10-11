
FROM python:3.9-slim

WORKDIR /app

COPY requerimentos.txt /app/

RUN pip install --no-cache-dir -r requerimentos.txt

COPY . /app

EXPOSE 5001

ENTRYPOINT ["python"]

CMD ["app.py"]
