To test on minikube:

```
minikube start
helm init --wait
helm install -f ../../helm-example-configs/minikube.yaml ../../biocontainers-backend
```

Then check pods and if failing, see the logs:

```
kubectl get pods
# check for pod name
kubectl logs -f <pod-name>
```

To make changes on the container:

```
# point docker engine to minikubes to avoid building and pushing to dockerhub between tests:
eval $(minikube docker-env)
# with this user you won't need to change the minikube yaml config, but change it if you want to push
docker build -t ypriverol/biocontainers-api-py:1.0.0 .
# Delete the pod (change pod name below)
kubectl delete pods/<pod-name>
# Get logs from new pod, after looking into `kubectl get pods`
```
