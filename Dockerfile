FROM python:slim
RUN apt update && apt install -y curl gcc make && curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
COPY . /app
WORKDIR /app
RUN $HOME/.poetry/bin/poetry config virtualenvs.create false && $HOME/.poetry/bin/poetry install --no-dev
EXPOSE 8000
CMD python web_api/main.py
