
#### 미니큐브 실행

- minikube start

#### 로컬pc 마운트트

- minikube mount "C:\volume:/data/mysql"

#### namespase 적용

- kubectl apply -f k8s/namespace.yml

#### 이미지 빌드

- minikube image build -t metacoding/db:1 ./db
- minikube image build -t metacoding/backend:1 ./backend
- minikube image build -t metacoding/frontend:1 ./frontend
- minikube image build -t metacoding/redis:1 ./redis

#### pod 생성

- kubectl apply -f k8s/db/db-pv.yml 
- kubectl apply -f k8s/ --recursive

### 결과 확인

- kubectl -n metacoding get deploy,pod,service

### 연결

- minikube service frontend-service -n metacoding --url (브라우저 접속 URL 확인)

### 오류 발생시 로그 확인

- kubectl -n metacoding logs deploy/db-deploy --tail=50
- kubectl -n metacoding logs deploy/frontend-deploy --tail=50
- kubectl -n metacoding logs deploy/backend-deploy --tail=100 (더 많은 로그 확인)
- kubectl -n metacoding logs deploy/backend-deploy --tail=200 | grep -i error (에러만 필터링)

### MySQL 초기화 오류 해결

MySQL이 "data directory has files in it" 오류를 발생시키는 경우:

```bash
# 1. DB Pod 삭제
kubectl -n metacoding delete pod -l app=db

# 2. 데이터 디렉토리 정리 (minikube 내부)
minikube ssh "sudo rm -rf /data/mysql/*"

# 3. Pod 재시작 (자동으로 재생성됨)
kubectl -n metacoding get pods
```

또는 로컬 PC 경로를 사용하는 경우:

```bash
# 1. DB Pod 삭제
kubectl -n metacoding delete pod -l app=db

# 2. 로컬 PC의 데이터 디렉토리 정리
# Windows: C:\volume\db 폴더 내용 삭제

# 3. Pod 재시작
kubectl -n metacoding get pods
```

### 백엔드 오류 해결

백엔드에서 스택 트레이스 오류가 발생하는 경우:

```bash
# 1. 전체 에러 메시지 확인 (더 많은 로그)
kubectl -n metacoding logs deploy/backend-deploy --tail=200

# 2. 에러만 필터링해서 확인
kubectl -n metacoding logs deploy/backend-deploy --tail=200 | grep -i "error\|exception\|failed"

# 3. 일반적인 원인 확인
# - DB 연결 오류: DB Pod 상태 확인
# - Redis 연결 오류: Redis Pod 상태 확인
# - 환경변수 오류: ConfigMap/Secret 확인

# 4. Pod 재시작
kubectl -n metacoding rollout restart deploy/backend-deploy
```

### DB 연결 오류 해결 (Communications link failure)

백엔드에서 "Communications link failure" 오류가 발생하는 경우:

```bash
# 1. DB Pod 상태 확인
kubectl -n metacoding get pods | grep db

# 2. DB Pod가 Running 상태인지 확인
kubectl -n metacoding get pods -l app=db

# 3. DB Pod 로그 확인
kubectl -n metacoding logs deploy/db-deploy --tail=50

# 4. DB Service 확인
kubectl -n metacoding get svc db-service

# 5. DB가 준비될 때까지 대기 후 백엔드 재시작
kubectl -n metacoding wait --for=condition=ready pod -l app=db --timeout=300s
kubectl -n metacoding rollout restart deploy/backend-deploy

# 6. 네트워크 연결 테스트 (백엔드 Pod에서)
kubectl -n metacoding exec -it <backend-pod-name> -- ping db-service
kubectl -n metacoding exec -it <backend-pod-name> -- telnet db-service 3306
```

### 전체 종료 (이미지 + 리소스)

#### 빠른 종료 (한 번에)

```bash
# 1. 모든 Kubernetes 리소스 삭제
kubectl delete namespace metacoding

# 2. PV 삭제 (namespace 외부에 있음)
kubectl delete pv db-pv

# 3. 미니큐브 내부 이미지 삭제
minikube ssh "docker rmi metacoding/db:1 metacoding/backend:1 metacoding/frontend:1 metacoding/redis:1 || true"

# 4. 미니큐브 중지
minikube stop
```

#### 상세 종료 방법

```bash
# 1. 모든 Kubernetes 리소스 삭제
kubectl delete namespace metacoding

# 2. PV 삭제 (클러스터 레벨 리소스)
kubectl delete pv db-pv

# 3. 미니큐브 내부 이미지 삭제
minikube ssh "docker rmi metacoding/db:1 metacoding/backend:1 metacoding/frontend:1 metacoding/redis:1 || true"

# 4. 미니큐브 중지 (데이터 유지)
minikube stop

# 5. 미니큐브 완전 삭제 (모든 데이터 삭제, 선택사항)
minikube delete
```

