FROM python:3.10-slim-buster
LABEL org.opencontainers.image.source https://github.com/flyteorg/flytesnacks

WORKDIR /root
ENV PYTHONPATH /root

RUN apt-get update && apt-get install build-essential -y \
    && apt-get clean autoclean \
    && apt-get autoremove --yes \
    && rm -rf /var/lib/{apt,dpkg,cache,log}/ \
    && useradd -u 1000 flytekit \
    && chown flytekit: /root \
    && chown flytekit: /home \
    && :

# Install Python dependencies
COPY requirements.txt /root
RUN pip install -r /root/requirements.txt
RUN pip freeze

# Copy the actual code
COPY . /root
