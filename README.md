깃허브의 https://github.com/luenarstery04/Team3-Project 링크로 들어간다.

https://velog.io/@dongvelop/Github-%ED%98%91%EC%97%85%ED%95%98%EA%B8%B0-PR%EB%B6%80%ED%84%B0-merge%EA%B9%8C%EC%A7%80

velog 링크를 통해 fork방법과 본인 Git으로 clone, branch 만드는 것까지 익힌다.

참고로 fork는 그냥 버튼만 누르면 된다. 본인 repository에 가져와진다.


파일 받아왔다면 .\venv\Scripts\activate 를 통해 가상환경 실행시켜본다.

실행 잘 된다면 MySQL 실행, 동봉된 Team3_Project_diagram.sql 열고

```
CREATE SCHEMA ssavi_db;

use ssavi_db;
```
까지만 실행한다.

이후 venv 환경으로 들어가

```cmd
python manage.py makemigrations
python manage.py migarte
```

차례로 실행해준다.

이제 남은 SQL문 실행하여 table 생성하여 오류 없는 지 확인한다.