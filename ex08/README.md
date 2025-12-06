
#### 미니큐브 실행

- minikube start

#### 이미지 빌드

- minikube image build -t metacoding/db:1 ./db
- minikube image build -t metacoding/backend:1 ./backend
- minikube image build -t metacoding/frontend:1 ./frontend
- minikube image build -t metacoding/redis:1 ./redis

#### namespase 적용

- kubectl apply -f k8s/namespace.yml

#### pod 생성

- kubectl apply -f k8s/ --recursive

### 결과 확인

- kubectl get deploy,pod,service -n metacoding

### 로그 확인

 - kubectl logs deploy/db-deploy -n metacoding --tail=100
 - kubectl logs deploy/frontend-deploy -n metacoding --tail=100
 - kubectl logs deploy/backend-deploy -n metacoding --tail=100

### 연결

- minikube service frontend-service -n metacoding --url