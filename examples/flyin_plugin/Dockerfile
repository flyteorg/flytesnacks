FROM python:3.10-slim-buster
LABEL org.opencontainers.image.source https://github.com/flyteorg/flytesnacks

WORKDIR /root
ENV PYTHONPATH /root

# Install Python dependencies
COPY requirements.txt /root
RUN pip install -r /root/requirements.txt
RUN pip freeze

# Copy the actual code
COPY . /root
