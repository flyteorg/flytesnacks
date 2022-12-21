FROM ghcr.io/flyteorg/flytekit:py3.10-1.2.5
WORKDIR /root

RUN apt-get update && apt-get install git curl -y

RUN pip install --no-deps -U "https://github.com/flyteorg/flytekit/archive/23c1798dd33ee6c7156fdf7b8395abe743710df3.zip#egg=flytekit"

COPY . /root



