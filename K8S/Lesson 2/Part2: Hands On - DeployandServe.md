           __   ___  __        ___ ___  ___  __  
|__/ |  | |__) |__  |__) |\ | |__   |  |__  /__` 
|  \ \__/ |__) |___ |  \ | \| |___  |  |___ .__/ 
 __        __     __   __  
|__)  /\  /__` | /  ` /__` 
|__) /~~\ .__/ | \__, .__/ 
                           

PART 2: Hands On Engineering - Configure an nginx deployment and service

Code you will use:

You will need to add these two yaml files to the directory in your cluster.



nginx-deployment.yaml



apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.16
        ports:
        - containerPort: 8080



nginx-service.yaml



apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080



Commands you will use:



kubectl apply -f nginx-deployment.yaml
kubectl apply -f nginx-service.yaml

kubectl get svc
kubectl get ep
kubectl get svc --show-labels
kubectl get svc -l app=nginx 
kubectl get pod --show-labels
kubectl get pod -l app=nginx
kubectl logs -l app=nginx
kubectl get pod -n kube-system --show-labels

kubectl scale --help
kubectl scale deployment nginx-deployment --replicas 4
kubectl scale deployment nginx-deployment --replicas 3
kubectl rollout history deployment nginx-deployment

kubectl run test-nginx-service --image=busybox
kubectl describe pod test-nginx-service
kubectl edit pod test-nginx-service
kubectl logs nginx-deployment-6d777db949-89t8p 