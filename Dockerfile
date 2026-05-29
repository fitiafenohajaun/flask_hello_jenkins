FROM python:3.12-slim

RUN useradd flask
WORKDIR /home/flask

ADD . .

RUN chmod a+x app.py test.py && \
    chown -R flask:flask /home/flask

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

USER flask

CMD ["flask", "run"]