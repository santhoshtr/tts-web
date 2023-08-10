FROM python:3.10-slim

WORKDIR /root

# We need to set the host to 0.0.0.0 to allow outside access
ENV HOST 0.0.0.0

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc g++ make python3 python3-dev python3-pip python3-venv python3-wheel espeak-ng libsndfile1-dev build-essential wget cmake && \
    rm -rf /var/lib/apt/lists/*

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /root

RUN rm -rf /root/.cache/pip

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]

EXPOSE 80
