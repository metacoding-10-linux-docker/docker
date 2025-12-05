
#### 미니큐브 실행

- minikube start

#### namespase 적용

- kubectl apply -f k8s/namespace.yml

#### 이미지 빌드

- minikube image build -t metacoding/db:1 ./db
- minikube image build -t metacoding/backend:1 ./backend
- minikube image build -t metacoding/frontend:1 ./frontend
- minikube image build -t metacoding/redis:1 ./redis

#### pod 생성

- kubectl apply -f k8s/ --recursive

### 결과 확인

- kubectl -n metacoding get deploy,pod,service

### 로그 확인

- kubectl -n metacoding logs deploy/db-deploy --tail=100
- kubectl -n metacoding logs deploy/frontend-deploy --tail=100
- kubectl -n metacoding logs deploy/backend-deploy --tail=100 

### 연결

- minikube service frontend-service -n metacoding --url (브라우저 접속 URL 확인)

