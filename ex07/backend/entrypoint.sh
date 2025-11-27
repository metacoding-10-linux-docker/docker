#!/bin/bash

git clone https://github.com/metacoding-10-linux-docker/backend-server 

cd backend-server

chmod +x gradlew 

./gradlew build  

java -jar -Dspring.profiles.active=prod build/libs/*.jar  