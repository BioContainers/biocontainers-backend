# MongoDB on Kubernetes with Stateful Sets
With the release of Stateful Sets and custom Storage Classes, Kubernetes can automate all of the underlying infra required to run a MongoDB Replica Sets
http://blog.kubernetes.io/2017/01/running-mongodb-on-kubernetes-with-statefulsets.html

### Creating Storage Class
You can create Storage Classes with different provisioners depending on your Kubernetes environment.

Minikube for local testing:
```
$ cd manifests/statefulset
$ kubectl apply -f mongo-storage.yml
```

Verify the Storage Class
```
$ kubectl get storageclass
```

### Creating Stateful Set
```
$ cd manifests/statefulset
$ kubectl apply -f mongo-statefulset.yaml
```

Verify the Stateful Set
```
$ kubectl get statefulset
```


### Creating Service
```
$ cd manifests/statefulset
$ kubectl apply -f mongo-service.yaml
```

Verify the Volumes
```
$ kubectl get pvc
```

### API Service
Rebuild api-service.
Recreate deploy and service.

### Reference
[Running MongoDB on Kubernetes with StatefulSets](https://github.com/cvallance/mongo-k8s-sidecar/tree/master/example/StatefulSet)