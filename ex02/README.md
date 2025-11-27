## 실행 명령어

### 서버 1 2개 생성

- docker build -t app1 ./app1

- docker run -dit -p 8000:80 app1
- docker run -dit -p 8001:80 app1

### nginx 실행

- docker build -t lb ./lb
- docker run -dit -p 80:80 lb

### 실행

- http://localhost:80/app1
