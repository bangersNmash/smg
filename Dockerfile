FROM python:3.7.7-slim-buster

EXPOSE 5000

WORKDIR /usr/src/server

RUN python3 -m pip install gunicorn

COPY requirements.txt ./
RUN python3 -m pip install -r requirements.txt

COPY server.py sql.py database.py properties.py db ./

ENTRYPOINT ["gunicorn"]
CMD ["server:APP", "-b", "0.0.0.0:5000"]
