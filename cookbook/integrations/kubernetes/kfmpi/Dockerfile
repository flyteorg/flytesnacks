FROM python:3.6-slim-buster

ENV HOROVOD_VERSION=0.19.0

ENV VENV /opt/venv

RUN apt-get update && apt-get install -y --allow-downgrades --allow-change-held-packages --no-install-recommends \
        build-essential \
        cmake \
        g++ \
        git \
        curl \
        vim \
        wget \
        ca-certificates \
        libjpeg-dev \
        libpng-dev \
        librdmacm1 \
        libibverbs1 \
        ibverbs-providers

# Virtual environment
RUN python3 -m venv ${VENV}
ENV PATH="${VENV}/bin:$PATH"

# Install the AWS cli separately to prevent issues with boto being written over
RUN pip install awscli

# Install Open MPI
RUN mkdir /tmp/openmpi && \
    cd /tmp/openmpi && \
    wget https://www.open-mpi.org/software/ompi/v4.0/downloads/openmpi-4.0.0.tar.gz && \
    tar zxf openmpi-4.0.0.tar.gz && \
    cd openmpi-4.0.0 && \
    ./configure --enable-orterun-prefix-by-default && \
    make -j $(nproc) all && \
    make install && \
    ldconfig && \
    rm -rf /tmp/openmpi

# Install OpenSSH for MPI to communicate between containers
RUN apt-get install -y --no-install-recommends openssh-client openssh-server && \
    mkdir -p /var/run/sshd

RUN sed -i 's/[ #]\(.*StrictHostKeyChecking \).*/ \1no/g' /etc/ssh/ssh_config && \
    echo "    UserKnownHostsFile /dev/null" >> /etc/ssh/ssh_config && \
    sed -i 's/#\(StrictModes \).*/\1no/g' /etc/ssh/sshd_config

# Install Python dependencies
COPY kfmpi/requirements.txt /root

RUN pip install -r /root/requirements.txt

# Install Horovod
RUN HOROVOD_WITH_TENSORFLOW=1 pip install  horovod

# Copy the makefile targets to expose on the container. This makes it easier to register.
COPY in_container.mk /root/Makefile
COPY kfmpi/sandbox.config /root

# Copy the actual code
COPY kfmpi/ /root/kfmpi/

# This tag is supplied by the build script and will be used to determine the version
# when registering tasks, workflows, and launch plans
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
