FROM python:3.8-buster

WORKDIR /root
ENV VENV /opt/venv
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH /root

# This is necessary for opencv to work
RUN apt-get update && apt-get install -y libsm6 libxext6 libxrender-dev ffmpeg

# Install the AWS cli separately to prevent issues with boto being written over
RUN pip3 install awscli

ENV VENV /opt/venv
# Virtual environment
RUN python3 -m venv ${VENV}
ENV PATH="${VENV}/bin:$PATH"

# Install Python dependencies
COPY ./requirements.txt /root
RUN pip install -r /root/requirements.txt

# Copy the actual code
COPY . /root

# This tag is supplied by the build script and will be used to determine the version
# when registering tasks, workflows, and launch plans
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag

# Because we have not released flytekit yet, we will use this git-sha
RUN pip install -U https://github.com/lyft/flytekit/archive/b26dc3404da841728921689ce4d81ee6695d2d88.zip#egg=flytekit[schema]
