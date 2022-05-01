FROM python:3.9

COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./src /app/src

ENV PYTHONPATH=/app/src

EXPOSE 80

RUN pip install --no-cache-dir -r /app/requirements.txt

# Run the start script, it start Gunicorn with Uvicorn
WORKDIR /app
CMD [ "python", "src/main.py" ]
