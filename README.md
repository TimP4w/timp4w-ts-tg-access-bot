# TeamSpeak Telegram Access Bot

A simple bot that notifies in a Telegram chat whenever someone enters a TeamSpeak server.

# Dev setup

```
$ pip install pipenv
$ pipenv install
```

## Run (Dev)

```
$ pipenv shell
$ python src/bot.py
```

# Build docker image

```
docker build . -t image-name:tag
```

On Apple Silicon it may be necessary to specify the platform if the image needs to be used on another machine

```
docker buildx build --platform=linux/amd64 . -t image-name:tag
```

# Run docker image

```
docker run --rm --env-file .env image-name:tag
```

# ENV file (.env)

```
TG_TOKEN=
TG_CHAT_ID=
TS_HOST=
TS_PWD=
TS_USER=
TS_PORT=
TS_CHANNEL=
```

# License (MIT)
[LICENSE](LICENSE.md)
