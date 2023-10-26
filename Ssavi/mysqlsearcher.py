import pymysql

class DBsearch:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        # 나의 ssavi_db에 연결한다.
        self.conn = pymysql.connect(host='localhost',
                                    port=3306,
                                    db='ssavi_db',
                                    user='root',
                                    passwd='Dluen886905!',
                                    charset='utf8')
        self.cursor = self.conn.cursor()

    def disconnect(self):
        # DB 접속 종료. 항상 마지막에 실행시켜줘야 한다.
        self.cursor.close()
        self.conn.close()

    def selectUserGenre(self, user_id):
        # 유저의 장르값을 가져와 album에서 조회한다.
        # 현재 제대로 작동하지 않는다. self를 찾을 수 없다고 한다.

        # 테스트용 가짜 번호
        fakeuser_id = 2
        self.connect()
        
        sql = 'SELECT user_genre FROM users_app_user WHERE id=' + user_id
        self.cursor.execute(sql)
        row_string = self.cursor.fetchall()

        genre_string = row_string[0][0]
        genre_list = genre_string.split(',')

        self.disconnect()

        return genre_list
        

    # def selectGenreDefault(self):
        # 유저가 마음에 들어하는 장르가 없거나 로그인하지 않았을 때
        # 기본값으로 보여줄 장르들이다.