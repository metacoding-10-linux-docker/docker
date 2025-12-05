
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
- kubectl apply -f k8s/db/db-pvc.yml

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

#### 방법 1: Deployment 스케일 다운 후 정리 (권장)

```bash
# 1. DB Deployment를 0으로 스케일 다운 (Pod 중지)
kubectl -n metacoding scale deploy db-deploy --replicas=0

# 2. 데이터 디렉토리 정리 (minikube 내부)
minikube ssh "sudo rm -rf /data/mysql/*"

# 3. Deployment를 다시 1로 스케일 업
kubectl -n metacoding scale deploy db-deploy --replicas=1

# 4. Pod 상태 확인
kubectl -n metacoding get pods -l app=db
```

#### 방법 2: Pod 강제 삭제 후 정리

```bash
# 1. DB Pod 강제 삭제
kubectl -n metacoding delete pod -l app=db --force --grace-period=0

# 2. 데이터 디렉토리 정리 (minikube 내부)
minikube ssh "sudo rm -rf /data/mysql/*"

# 3. Pod 자동 재생성 확인
kubectl -n metacoding get pods -l app=db
```

#### 로컬 PC 경로를 사용하는 경우:

```bash
# 1. DB Deployment를 0으로 스케일 다운
kubectl -n metacoding scale deploy db-deploy --replicas=0

# 2. Windows에서 로컬 경로 정리
# C:\volume\mysql 폴더 내용 삭제 (또는 폴더 자체 삭제)

# 3. Deployment를 다시 1로 스케일 업
kubectl -n metacoding scale deploy db-deploy --replicas=1

# 4. Pod 상태 확인
kubectl -n metacoding get pods -l app=db
```

### 로컬 데이터 사용하기

미니큐브를 재실행했을 때 로컬에 있는 데이터를 사용하려면:

#### MySQL 동작 방식

- **데이터 디렉토리가 비어있음**: 초기화 실행 (init.sql 실행)
- **데이터 디렉토리에 완전한 MySQL 데이터가 있음**: 기존 데이터 사용 (init.sql 실행 안 함)
- **데이터 디렉토리에 불완전한 파일이 있음**: 오류 발생

#### 해결 방법

**옵션 1: 완전히 초기화된 데이터 사용 (권장)**

```bash
# 1. 처음 한 번만 초기화 (데이터 디렉토리 비우기)
kubectl -n metacoding scale deploy db-deploy --replicas=0
minikube ssh "sudo rm -rf /data/mysql/*"
kubectl -n metacoding scale deploy db-deploy --replicas=1

# 2. MySQL이 완전히 초기화될 때까지 대기
kubectl -n metacoding wait --for=condition=ready pod -l app=db --timeout=300s

# 3. 이후부터는 데이터가 유지되므로 그대로 사용 가능
# 미니큐브를 재시작해도 데이터가 유지됨
```

**옵션 2: 기존 데이터 백업 후 복원**

```bash
# 1. 기존 데이터 백업
kubectl -n metacoding exec -it <db-pod-name> -- mysqldump -u root -p metadb > backup.sql

# 2. 새로 초기화
kubectl -n metacoding scale deploy db-deploy --replicas=0
minikube ssh "sudo rm -rf /data/mysql/*"
kubectl -n metacoding scale deploy db-deploy --replicas=1

# 3. 데이터 복원
kubectl -n metacoding exec -i <db-pod-name> -- mysql -u root -p metadb < backup.sql
```

**옵션 3: 불완전한 파일만 정리**

```bash
# 불완전한 초기화 파일만 삭제 (데이터는 유지)
kubectl -n metacoding scale deploy db-deploy --replicas=0
minikube ssh "sudo rm -rf /data/mysql/*.pid /data/mysql/*.err /data/mysql/ib_logfile*"
kubectl -n metacoding scale deploy db-deploy --replicas=1
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

