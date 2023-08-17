FROM ubuntu:focal
LABEL org.opencontainers.image.source https://github.com/flyteorg/flytesnacks

WORKDIR /root
ENV VENV /opt/venv
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH /root
ENV DEBIAN_FRONTEND=noninteractive

# Install Python3.10 and other libraries
RUN apt-get update \
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:ubuntu-toolchain-r/test \
    && add-apt-repository -y ppa:deadsnakes/ppa \
    && apt-get install -y \
    build-essential \
    cmake \
    g++-7 \
    curl \
    git \
    wget \
    python3.10 \
    python3.10-venv \
    python3.10-dev \
    make \
    libssl-dev \
    python3-pip \
    python3-wheel \
    libuv1

# Virtual environment
ENV VENV /opt/venv
RUN python3.10 -m venv ${VENV}
ENV PATH="${VENV}/bin:$PATH"

# Install wheel after venv is activated
RUN pip3 install wheel

# Install Open MPI
RUN wget --progress=dot:mega -O /tmp/openmpi-4.1.4-bin.tar.gz https://download.open-mpi.org/release/open-mpi/v4.1/openmpi-4.1.4.tar.gz && \
    cd /tmp && tar -zxf /tmp/openmpi-4.1.4-bin.tar.gz && \
    mkdir openmpi-4.1.4/build && cd openmpi-4.1.4/build && ../configure --prefix=/usr/local && \
    make -j all && make install && ldconfig && \
    mpirun --version

# Allow OpenSSH to talk to containers without asking for confirmation
RUN mkdir -p /var/run/sshd
RUN cat /etc/ssh/ssh_config | grep -v StrictHostKeyChecking > /etc/ssh/ssh_config.new && \
    echo "    StrictHostKeyChecking no" >> /etc/ssh/ssh_config.new && \
    mv /etc/ssh/ssh_config.new /etc/ssh/ssh_config

# Install Python dependencies
COPY requirements.txt /root
RUN pip install -r /root/requirements.txt

# Install TensorFlow
# In case you encounter the "The TensorFlow library was compiled to use AVX instructions, which are not present on your machine" error,
# you can resolve it by installing TensorFlow using the following RUN instruction:
# RUN wget https://tf.novaal.de/westmere/tensorflow-2.8.0-cp310-cp310-linux_x86_64.whl && pip install tensorflow-2.8.0-cp310-cp310-linux_x86_64.whl
# Otherwise:
RUN pip install tensorflow==2.8.0

# Enable GPU
# ENV HOROVOD_GPU_OPERATIONS NCCL
RUN HOROVOD_WITH_MPI=1 pip install --no-cache-dir horovod==0.28.1

# Copy the actual code
COPY . /root/

# This tag is supplied by the build script and will be used to determine the version
# when registering tasks, workflows, and launch plans
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
