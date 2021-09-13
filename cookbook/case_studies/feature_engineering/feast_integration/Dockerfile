FROM python:3.8-buster

WORKDIR /root
ENV VENV /opt/venv
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH /root
ENV FEAST_S3_ENDPOINT_URL http://localhost:30084/
ENV AWS_ACCESS_KEY_ID minio
ENV AWS_SECRET_ACCESS_KEY miniostorage

# Install the AWS cli separately to prevent issues with boto being written over
RUN pip3 install awscli

# Virtual environment
RUN python3 -m venv ${VENV}
RUN ${VENV}/bin/pip install wheel
ENV PATH="${VENV}/bin:$PATH"

# Install Python dependencies
COPY feast_integration/requirements.txt /root/.
RUN ${VENV}/bin/pip install -r /root/requirements.txt

COPY feast_integration/sandbox.config /root/
COPY in_container.mk /root/Makefile

# Copy the actual co
COPY feast_integration/ /root/feast_integration/

# Copy minio credentials to known place
COPY feast_integration/aws.config /root/.aws/config

# This tag is supplied by the build script and will be used to determine the version
# when registering tasks, workflows, and launch plans
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag

# Copy over the helper script that the SDK relies on
RUN cp ${VENV}/bin/flytekit_venv /usr/local/bin/
RUN chmod a+x /usr/local/bin/flytekit_venv

# Enable the virtualenv for this image. Note this relies on the VENV variable we've set in this image.
ENTRYPOINT ["/usr/local/bin/flytekit_venv"]
