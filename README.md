# covid-19-kr-slack-notifier

##### 코로나바이러스감염증-19 데이터를 가져와 슬랙 Web Hook으로 보내줍니다.
##### `hook_url.conf` 파일을 만들고, 그 안에 Web Hook URL만 넣어주면됩니다.


### 실행하기
```
python3 ./notifier.py
```


### 활용
##### AWS Lambda와 함께 쓰면 편합니다.
##### Lambda 구성이 귀찮으면 crontab과 함께써도 되겠죠. 아래처럼 설정하면 매일 오전 10시 30분에 알림이 오게 됩니다.
##### 30 10 * * *
