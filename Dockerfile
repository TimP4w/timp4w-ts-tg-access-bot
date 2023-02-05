FROM python:3.10-slim 

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

# Install pipenv
RUN pip install pipenv

# Install python deps
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --system --deploy --ignore-pipfile

# Setup bot env
ENV TS_HOST=
ENV TS_PWD=
ENV TS_USER=serveradmin
ENV TS_PORT=10011
ENV TS_CHANNEL='Default'
ENV TG_TOKEN=
ENV TG_CHAT_ID=

# Create user to avoid using root
RUN useradd --create-home tgtsbot
WORKDIR /home/tgtsbot
USER tgtsbot

COPY . .

ENTRYPOINT ["python3", "-u", "./src/bot.py"]
