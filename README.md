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
