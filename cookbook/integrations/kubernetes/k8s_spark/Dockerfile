FROM apache/spark-py:v3.2.2
LABEL org.opencontainers.image.source https://github.com/flyteorg/flytesnacks

WORKDIR /root
ENV VENV /opt/venv
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH /root
ENV DEBIAN_FRONTEND=noninteractive

## Install Python3 and other basics
USER 0
RUN apt-get update && apt-get install -y python3 python3-venv make build-essential libssl-dev python3-pip curl wget

# Install AWS CLI to run on AWS (for GCS install GSutil). This will be removed
# in future versions to make it completely portable
RUN pip3 install awscli

WORKDIR /opt
RUN curl https://sdk.cloud.google.com > install.sh
RUN bash /opt/install.sh --install-dir=/opt
ENV PATH $PATH:/opt/google-cloud-sdk/bin
WORKDIR /root

# Virtual environment
ENV VENV /opt/venv
RUN python3 -m venv ${VENV}
ENV PATH="${VENV}/bin:$PATH"
RUN pip3 install wheel

# Install Python dependencies
COPY k8s_spark/requirements.txt /root
RUN pip install -r /root/requirements.txt

RUN wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-common/3.3.2/hadoop-common-3.3.2.jar -P /opt/spark/jars && \
    wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.2/hadoop-aws-3.3.2.jar -P /opt/spark/jars && \
    wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.1026/aws-java-sdk-bundle-1.11.1026.jar -P /opt/spark/jars

# ENV SPARK_HOME /opt/spark
# ENV SPARK_VERSION 3.2.2
# ENV PYSPARK_PYTHON ${VENV}/bin/python3
# ENV PYSPARK_DRIVER_PYTHON ${VENV}/bin/python3

# Copy the makefile targets to expose on the container. This makes it easier to register.
# Delete this after we update CI
COPY in_container.mk /root/Makefile

# Delete this after we update CI to not serialize inside the container
COPY k8s_spark/sandbox.config /root

# Copy the actual code
COPY k8s_spark/ /root/k8s_spark

# This tag is supplied by the build script and will be used to determine the version
# when registering tasks, workflows, and launch plans
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag

# Copy over the helper script that the SDK relies on
RUN cp ${VENV}/bin/flytekit_venv /usr/local/bin/
RUN chmod a+x /usr/local/bin/flytekit_venv

# For spark we want to use the default entrypoint which is part of the
# distribution, also enable the virtualenv for this image.
ENTRYPOINT ["/opt/entrypoint.sh"]
