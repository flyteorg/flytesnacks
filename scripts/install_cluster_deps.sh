#!/usr/bin/env bash

set -e

PLATFORM="$(uname | tr '[:upper:]' '[:lower:]')"

get_k3d() {
    local target_dir="$1"
    local executable="${target_dir}/k3d"
    local version="${K3D_VERSION:-v4.2.0}"

    ( [ -f ${executable} ] && $(${executable} --version | grep -q "k3d version ${version}") ) || curl -s https://raw.githubusercontent.com/rancher/k3d/main/install.sh | USE_SUDO=false K3D_INSTALL_DIR=${target_dir} TAG="${version}" bash > /dev/null
}

get_k3c() {
    local target_dir="$1"
    local executable="${target_dir}/k3c"
    local version="${K3C_VERSION:-v0.3.0-alpha.0}"

    # TODO: determine arm vs amd64 architecture
    ( [ -f ${executable} ] && $(${executable} --version | grep -q "k3c version ${version}") ) || ( curl -L -o ${executable} https://github.com/rancher/k3c/releases/download/${version}/k3c-${PLATFORM}-amd64 && chmod +x ${executable} )
}

get_kubectl() {
    local executable="$1/kubectl"
    local version="${KUBECTL_VERSION:-v1.20.2}"

    ( [ -f ${executable} ] && $(${executable} version | grep -q "GitVersion:\"${version}\"") ) || ( curl -L -o ${executable} https://dl.k8s.io/release/${version}/bin/${PLATFORM}/amd64/kubectl && chmod +x ${executable} )
}

mkdir -p _bin
for dep in k3d k3c kubectl; do
    "get_${dep}" _bin
done
