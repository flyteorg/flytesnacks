#syntax=docker/dockerfile:1.8
FROM python:3.8-buster

WORKDIR /root
ENV VENV /opt/venv
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH /root

# Install the AWS cli separately to prevent issues with boto being written over
RUN pip3 install awscli

# Install gcloud for GCP
RUN apt-get update && apt-get install -y curl

WORKDIR /opt
RUN curl https://sdk.cloud.google.com > install.sh
RUN bash /opt/install.sh --install-dir=/opt
ENV PATH $PATH:/opt/google-cloud-sdk/bin
WORKDIR /root

ENV VENV /opt/venv
# Virtual environment
RUN python3 -m venv ${VENV}
ENV PATH="${VENV}/bin:$PATH"

# Install Python dependencies
COPY requirements.in /root/
RUN --mount=type=cache,sharing=locked,mode=0777,target=/root/.cache/pip,id=pip \
    pip install -r /root/requirements.in

# Copy the actual code
COPY . /root/

# This tag is supplied by the build script and will be used to determine the version
# when registering tasks, workflows, and launch plans
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
