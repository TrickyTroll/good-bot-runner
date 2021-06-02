docker pull docker pull trickytroll/good-bot-runner:latest

docker run --rm --name runner -v $PWD:. good-bot-runner:latest passwords.yaml
docker run --rm --name ssh-tester -it -p 7655:22 ubuntu:latest /bin/bash