## 실행 명령어

### api 서버 실행

docker build -t api ./api
docker run -dit -p 5000:5000 api

### nginx 실행

docker build -t nginx ./nginx
docker run -dit -p 80:80 nginx

### 실행

- http://localhost:80
- http://localhost:80/image.png
