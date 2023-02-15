FROM ubuntu:focal

ENV VENV /opt/venv
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH /root

RUN apt-get update \
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get install -y \
    && apt-get update \
    && apt-get install -y \
    cmake \
    curl \
    python3.8 \
    python3.8-venv \
    python3.8-dev \
    make \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-pip \
    zlib1g-dev \
    vim \
    wget

# Install the AWS cli separately to prevent issues with boto being written over
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

# Download BLAST
RUN wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.13.0/ncbi-blast-2.13.0+-x64-linux.tar.gz && \
    tar -xzf ncbi-blast-2.13.0+-x64-linux.tar.gz

# Set the working directory
WORKDIR /root

# Install Python dependencies
COPY blast/requirements.txt /root
RUN ${VENV}/bin/pip install -r /root/requirements.txt

# Copy the makefile targets to expose on the container. This makes it easier to register.
COPY in_container.mk /root/Makefile
COPY blast/sandbox.config /root

# Copy data
# COPY blast/kitasatospora /root/kitasatospora

# Copy the actual code
COPY blast/ /root/bioinformatics/blast/

# Copy over the helper script that the SDK relies on
RUN cp ${VENV}/bin/flytekit_venv /usr/local/bin/
RUN chmod a+x /usr/local/bin/flytekit_venv

# Check if BLAST is installed
ENV PATH=$PATH:/root/ncbi-blast-2.13.0+/bin
RUN echo $PATH
RUN output="$(which blastx)" && echo $output

# This tag is supplied by the build script and will be used to determine the version
# when registering tasks, workflows, and launch plans
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
