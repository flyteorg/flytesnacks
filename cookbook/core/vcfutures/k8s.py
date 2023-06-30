from typing import List
from flytekitplugins.pod import Pod
from kubernetes.client.models import (
    V1PodSpec,
    V1Container,
    V1EmptyDirVolumeSource,
    V1PodSpec,
    V1ResourceRequirements,
    V1Volume,
    V1VolumeMount,
    V1EnvVar,
    V1EnvFromSource,
    V1ConfigMapEnvSource,
    V1SecretEnvSource,
    V1Toleration,
)

def k8s_env(env_dict) -> List[V1EnvVar]:
    return [V1EnvVar(name=k, value=v) for k, v in env_dict.items()]

def k8s_env_from_configmap(cms) -> List[V1EnvFromSource]:
    return [V1EnvFromSource(config_map_ref=V1ConfigMapEnvSource(name=cm)) for cm in cms]

def k8s_env_from_secret(secrets) -> List[V1EnvFromSource]:
    return [V1EnvFromSource(secret_ref=V1SecretEnvSource(name=secret)) for secret in secrets]

def task_config(image: str, **kwargs):
    cache = kwargs.get("cache", False)
    primary_container_name = kwargs.get("primary_container_name", "primary")
    env = kwargs.get("env", {})
    env_configmaps = kwargs.get("env_configmaps", [])
    env_secrets = kwargs.get("env_secrets", [])
    node_pool = kwargs.get("node_pool", "default-pool")
    cpu_request = kwargs.get("cpu", kwargs.get("cpu_request", "1"))
    cpu_limit = kwargs.get("cpu", kwargs.get("cpu_limit", "1"))
    memory_request = kwargs.get("memory", kwargs.get("memory_request", "1Gi"))
    memory_limit = kwargs.get("memory", kwargs.get("memory_limit", "1Gi"))
    gpu = int(kwargs.get("gpu", 0))
    mount_shared_memory = kwargs.get("mount_shared_memory", False)

    # Hard-coded default environment variables for all tasks
    default_env = {
        "PYTHONUNBUFFERED": "1"
    }

    env.update(default_env)

    env_from_sources = k8s_env_from_configmap(env_configmaps) + k8s_env_from_secret(env_secrets)

    resource_requests = {"cpu": cpu_request, "memory": memory_request}
    resource_limits = {"cpu": cpu_limit, "memory": memory_limit}

    if gpu > 0:
        resource_requests["nvidia.com/gpu"] = gpu
        resource_limits["nvidia.com/gpu"] = gpu

    volumes = []
    volume_mounts = []

    if mount_shared_memory:
        dshm_volume = V1Volume(
            name="dshm",
            empty_dir=V1EmptyDirVolumeSource(medium="Memory")
        )
        volumes.append(dshm_volume)

        dshm_volume_mount = V1VolumeMount(
            mount_path="/dev/shm",
            name="dshm"
        )
        volume_mounts.append(dshm_volume_mount)

    pod = Pod(pod_spec=V1PodSpec(
        containers=[V1Container(
            name=primary_container_name,
            env=k8s_env(env),
            env_from=env_from_sources,
            resources=V1ResourceRequirements(
                requests=resource_requests,
                limits=resource_limits,
            ),
            volume_mounts=volume_mounts,
        )],
        volumes=volumes,
        node_selector={"cloud.google.com/gke-nodepool": node_pool},
        tolerations=[
            V1Toleration(
                key="nodepool",
                operator="Equal",
                value=node_pool,
                effect="NoSchedule",
            ),
            V1Toleration(
                key='nvidia.com/gpu',
                operator='Exists',
                effect='NoSchedule',
            ),
        ],
    ))

    return {
        'task_config': pod,
        'container_image': image, # Must match pod spec's image
        'cache': cache,
        'cache_serialize': cache,
        'cache_version': "xyz", # Change this string to invalidate all existing cache, it can be set to  any string
    }
