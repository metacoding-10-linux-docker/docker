## 실행 명령어

### 네트워크 만들기

- docker network create rnet

### redis 앱 빌드 및 실행

- docker run -d --name redis --network rnet -p 6379:6379 redis

### api 실행

- docker build -t api ./api
- docker run -d --name api1 --network rnet -p 5001:5000 api
- docker run -d --name api2 --network rnet -p 5002:5000 api

### 실행

- http://localhost:5001/save
- http://localhost:5002/read

### tcp 오류 발생 시

- netsh interface ipv4 show excludedportrange protocol=tcp
- net stop winnat
