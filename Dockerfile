FROM python3.9

ENV PYTHONPATH=/app
ENV PORT=8000

RUN pip install --upgrade pip

COPY ./requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./src /app/src

WORKDIR /app

CMD [ "python", "src/main.py" ]
