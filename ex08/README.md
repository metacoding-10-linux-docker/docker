## 실행 명령어

### 미니큐브 실행

- minikube start

### namespase 적용

- kubectl apply -f k8s/namespace.yml

### 이미지 빌드

- minikube image build -t metacoding/mysql:1 ./db
- minikube image build -t metacoding/backend:1 ./backend
- minikube image build -t metacoding/frontend:1 ./frontend

### pod 생성

- kubectl apply -f k8s/db/secret.yml
- kubectl apply -f k8s/db/pvc.yml
- kubectl apply -f k8s/db/deploy.yml
- kubectl apply -f k8s/db/service.yml

- kubectl apply -f k8s/backend/deploy.yml
- kubectl apply -f k8s/backend/service.yml

- kubectl apply -f k8s/frontend/deploy.yml
- kubectl apply -f k8s/frontend/service.yml

### 결과 확인

- kubectl -n metacoding get deploy,pod,service,ing

### 실행

- minikube service frontend -n metacoding --url (브라우저 접속 URL 확인)

### 오류 발생시 로그 확인

- kubectl -n metacoding logs deploy/db --tail=50
- kubectl -n metacoding logs deploy/frontend --tail=50
- kubectl -n metacoding logs deploy/backend --tail=50

### 미니큐브 종료

- minikube stop
