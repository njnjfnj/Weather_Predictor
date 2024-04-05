FROM python:3.10-slim

WORKDIR weather/

COPY src/requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN mkdir src && mkdir data

COPY data ./data 
COPY src ./src

ENV FLASK_APP=./src/api/app.py
EXPOSE 4000

CMD ["sh", "-c", "cd /weather/src/redis/seed/ && python3 seed.py && cd /weather/ && flask run --host=0.0.0.0 --port=4000 --debug"]

