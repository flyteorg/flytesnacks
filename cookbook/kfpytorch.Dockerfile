FROM pytorch/pytorch:1.7.0-cuda11.0-cudnn8-runtime

WORKDIR /root
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH /root

# Install the AWS cli separately to prevent issues with boto being written over
RUN pip install awscli

ENV VENV /opt/venv
# Virtual environment
RUN python3 -m venv ${VENV}
ENV PATH="${VENV}/bin:$PATH"

# Install Python dependencies
COPY ./recipes/plugins/kfpytorch/requirements.txt /root
RUN pip install -r /root/requirements.txt

# Copy the actual code
COPY . /root

# This tag is supplied by the build script and will be used to determine the version
# when registering tasks, workflows, and launch plans
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
