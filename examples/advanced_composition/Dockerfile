# ######################
# NOTE: For CI/CD only #
########################
FROM python:3.11-slim-buster
LABEL org.opencontainers.image.source https://github.com/flyteorg/flytesnacks

WORKDIR /root
ENV VENV /opt/venv
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH /root

RUN apt-get update && apt-get install -y build-essential curl git

# Virtual environment
ENV VENV /opt/venv
RUN python3 -m venv ${VENV}
ENV PATH="${VENV}/bin:$PATH"

RUN pip install flytekit==1.10.2
RUN pip install --no-deps -U --force-reinstall "git+https://github.com/flyteorg/flytekit.git@7eed0c024f60d5a633963e5a30cc5abd8972982a"
RUN pip install --no-deps -U --force-reinstall "git+https://github.com/flyteorg/flyte.git@v1.10.7-b4#subdirectory=flyteidl"

# Copy the actual code
COPY . /root

# This tag is supplied by the build script and will be used to determine the version
# when registering tasks, workflows, and launch plans
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
