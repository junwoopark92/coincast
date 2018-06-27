# coincast

The MIT License (MIT)
Copyright © 2018 <copyright holders>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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
