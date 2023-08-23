# ######################
# NOTE: For CI/CD only #
########################
FROM apache/spark-py:3.3.1
LABEL org.opencontainers.image.source https://github.com/flyteorg/flytesnacks

WORKDIR /root
ENV VENV /opt/venv
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH /root
ENV DEBIAN_FRONTEND=noninteractive
ARG spark_uid=1001

## Install Python3 and other basics
USER 0
RUN apt-get update && apt-get install -y python3 python3-venv make build-essential libssl-dev python3-pip curl wget

# Virtual environment
ENV VENV /opt/venv
RUN python3 -m venv ${VENV}
ENV PATH="${VENV}/bin:$PATH"
RUN pip3 install wheel

# Install Python dependencies
COPY requirements.txt /root
RUN pip install -r /root/requirements.txt

RUN wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.2.2/hadoop-aws-3.2.2.jar -P /opt/spark/jars && \
    wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar -P /opt/spark/jars

# Copy the actual code
COPY . /root/

# This tag is supplied by the build script and will be used to determine the version
# when registering tasks, workflows, and launch plans
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag

# Set /root user and group
RUN chown -R ${spark_uid}:${spark_uid} /root

# For spark we want to use the default entrypoint which is part of the
# distribution, also enable the virtualenv for this image.
ENTRYPOINT ["/opt/entrypoint.sh"]

ENV HOME /root
USER ${spark_uid}
