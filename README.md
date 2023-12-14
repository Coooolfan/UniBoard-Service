# UniBoard-Service

Connect and view all your device (service). 

### Run with docker

###### download Docker file from GitHub. 

```shell
mkdir  UniBoard-Service
cd UniBoard-Service
mkdir data

wget https://raw.githubusercontent.com/Coooolfan/UniBoard-Service/main/docker-compose.yml
wget https://raw.githubusercontent.com/Coooolfan/UniBoard-Service/main/Dockerfile
wget https://raw.githubusercontent.com/Coooolfan/UniBoard-Service/main/.env.example
wget https://raw.githubusercontent.com/Coooolfan/UniBoard-Service/main/config.json.example

cp .env.example .env
cp config.json.example config.json

```

###### edit `.env` and `config.json` .

###### run docker compose. 

```shell
docker compose up -d
```

or

```shell
docker-compose up -d
```



