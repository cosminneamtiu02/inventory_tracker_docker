# inventory_tracker_docker

cd C:\Program Files\Google\Chrome\Application

chrome.exe --disable-web-security --user-data-dir="C:/chrome-dev"

docker-compose up --build


# Instructiuni kubernetes

kubectl apply -f k8s/namespace.yaml

kubectl config set-context --current --namespace=myapp-namespace

kubectl apply -f k8s/secret.yaml

kubectl apply -f k8s/configmap.yaml

kubectl apply -f k8s/pv.yaml

kubectl apply -f k8s/pvc.yaml

kubectl apply -f k8s/postgres-deployment.yaml

kubectl apply -f k8s/postgres-service.yaml

kubectl apply -f k8s/backend-deployment.yaml

kubectl apply -f k8s/backend-service.yaml

kubectl apply -f k8s/ingress-nginx-deploy.yaml


# test

kubectl get pods

kubectl get deployment

kubectl get services


