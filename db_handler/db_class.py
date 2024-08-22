import psycopg


class DatabaseManager:
    def __init__(self, db_name='postgres', user='postgres', password='020722', host='localhost', port=5432):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = psycopg.connect(
            dbname=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )

    def connect(self):
        try:
            self.connection = psycopg.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            print("Подключение к базе данных успешно.")
        except Exception as e:
            print(f"Ошибка подключения: {e}")

    def add_user(self, tgID: int, username: str):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('INSERT INTO users (tgID, username) VALUES (%s, %s) ON CONFLICT (tgID) DO NOTHING',
                               (tgID,
                                username))
                print('Занесен')
        except Exception as e:
            print(f'Ошибка: {e}')

    def users(self, ):
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT * FROM users')
            print('d: ', cursor.fetchall())
