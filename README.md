# coincast

# 서버셋팅
## mysql server
https://hub.docker.com/r/mysql/mysql-server/

```
docker run --name my-container-name -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql/mysql-server:tag
docker exec -it my-container-name mysql -uroot -p
```
권한설정
https://stackoverflow.com/questions/17425523/python-mysql-operationalerror-1045-access-denied-for-user-rootlocalhost

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
cron으로 api crawler등록

```
$crontab -e
* * * * * python crontest.py >> cron.log

$service cron reload
```
- shell script사용하여 환경변수를 잡아야함

서버 시간 설정
```
tzselect
export TZ='Asia/Seoul'
```
python3 mysql client 설치
```
pip install mysqlclient
```
