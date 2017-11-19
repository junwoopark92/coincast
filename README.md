# coincast

# 서버셋팅
## mysql server
https://hub.docker.com/r/mysql/mysql-server/

```
docker run --name my-container-name -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql/mysql-server:tag
docker exec -it my-container-name mysql -uroot -p
```

## batch server
ubuntu + anaconda

python batch를 crontab으로 실행시킬 서버를 생성
```
docker pull continuumio/anaconda
docker run -it --name batch-server /bin/bash
```

docker container에서 가상환경 생성
```
conda create --name crawler python=3.5 anaconda
source activate crawler
```
