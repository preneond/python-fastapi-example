FROM python:3.10

COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./src /app/src

COPY ./appsettings.yaml /app/appsettings.yaml

ENV PYTHONPATH=/app

EXPOSE 8000

RUN pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app
CMD [ "python", "src/main.py" ]
