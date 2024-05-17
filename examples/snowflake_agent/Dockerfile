FROM python:3.8-slim-buster
LABEL org.opencontainers.image.source=https://github.com/flyteorg/flytesnacks

WORKDIR /root
ENV VENV /opt/venv
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH /root


# Install Python dependencies
COPY requirements.in /root
RUN pip install -r /root/requirements.in
RUN pip freeze

# Copy the actual code
COPY . /root/


# This tag is supplied by the build script and will be used to determine the version
# when registering tasks, workflows, and launch plans
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
