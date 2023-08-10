# TTS web interface

Supports scanning images and pdfs.

Use prebuilt docker image:
```
docker run -p 3000:80 ghcr.io/santhoshtr/tts-web:latest
```
Open http://0.0.0.0:3000/ using browser

OR

Checkout this repository and
```
docker build -t tts-web .
docker run -dp 3000:80 tts-web:latest
```
then
Open http://0.0.0.0:3000/ using browser
