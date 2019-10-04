# Using Debian because alpine doesn't have pipenv packaged :(
FROM python:3.7-slim-buster
WORKDIR /code
ENV FLASK_APP landtech/web.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV PYTHONPATH /code
COPY . .
RUN apt update && apt install -y pipenv && apt clean
RUN pipenv install
CMD ["pipenv", "run", "flask", "run"]
