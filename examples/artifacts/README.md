

## Commands

todo - need to multiarch this

docker build -f Dockerfile.artifact -t ghcr.io/unionai-oss/artifacts:v7 .
docker push ghcr.io/unionai-oss/artifacts:v7

Register the workflows
pyflyte -c ~/.flyte/local_admin.yaml register --image ghcr.io/unionai-oss/artifacts:v7 artifacts/ml_demo.py

Activate/Archive Launch Plan
flytectl -c ~/.flyte/local_admin.yaml update launchplan -p flytesnacks -d development scheduled_gather_data_lp --version JhBCVA_5PRtZ7TeHNoVkFA== --activate

## Setup

Redis
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flyte-sandbox-redis
  namespace: flyte
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/instance: flyte-sandbox
      app.kubernetes.io/name: redis
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app.kubernetes.io/instance: flyte-sandbox
        app.kubernetes.io/name: redis
    spec:
      containers:
      - name: master
        image: redis
        resources:
          requests:
            cpu: 300m
            memory: 500Mi
        ports:
        - containerPort: 6379
      dnsPolicy: ClusterFirst
      restartPolicy: Always
```
need to port forward this
