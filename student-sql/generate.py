# import os
# import datetime
# import pandas as pd
# import numpy as np
# from clickhouse_connect import get_client
#
# CH_USER = 'default'
# CH_PASSWORD = 'password12345'
#
# TOTAL_ROWS = 10000000
# print(TOTAL_ROWS)
#
# start_timestamp = int(datetime.datetime(2026, 1, 1).timestamp())
# random_seconds = np.random.randint(0, 10000000, size=TOTAL_ROWS, dtype=np.int32)
# timestamps = pd.to_datetime(start_timestamp + random_seconds, unit='s')
#
# df = pd.DataFrame({
#     'user_id': np.random.randint(1, 100000, size=TOTAL_ROWS, dtype=np.uint64),
#     'timestamp': timestamps,
#     'url': np.random.choice(['/home', '/cart', '/api', '/profile', '/payment'], size=TOTAL_ROWS),
#     'status_code': np.random.choice([200, 201, 401, 403, 404, 500, 502, 503], size=TOTAL_ROWS).astype(np.uint16)
# })
#
#
# print("Подключение к ClickHouse")
# client = get_client(host='localhost', port=8123, username=CH_USER, password=CH_PASSWORD)
#
# client.insert_df('logs_ch', df)
#
# print("Все успешно загружено")
#


import os
import io
import datetime
import pandas as pd
import numpy as np
import psycopg2

# 1. Чтение переменных из .env (ищем на уровень выше в корне IT1-Infra)
env_vars = {}
env_path = os.path.join('..', '.env') if os.path.exists(os.path.join('..', '.env')) else '.env'

if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, val = line.strip().split('=', 1)
                env_vars[key] = val

pg_user = env_vars.get('POSTGRES_USER', 'IT1_user')
pg_password = env_vars.get('POSTGRES_PASSWORD', 'password12345')
pg_db = env_vars.get('POSTGRES_DB', 'IT1_db')
pg_port = env_vars.get('POSTGRES_PORT', '5432')

# 2. Генерация 10 млн строк через Pandas в памяти
TOTAL_ROWS = 10000000
print(f"Генерация {TOTAL_ROWS} строк для PostgreSQL в памяти...")

start_timestamp = int(datetime.datetime(2026, 1, 1).timestamp())
random_seconds = np.random.randint(0, 10000000, size=TOTAL_ROWS, dtype=np.int32)
timestamps = pd.to_datetime(start_timestamp + random_seconds, unit='s')

df = pd.DataFrame({
    'user_id': np.random.randint(1, 100000, size=TOTAL_ROWS, dtype=np.int64),
    'timestamp': timestamps,
    'url': np.random.choice(['/home', '/cart', '/api', '/profile', '/payment'], size=TOTAL_ROWS),
    'status_code': np.random.choice([200, 401, 403, 404, 500], size=TOTAL_ROWS).astype(np.int32)
})

# 3. Подключение к PostgreSQL и сверхбыстрая запись через COPY
print("Подключение к PostgreSQL...")
conn = psycopg2.connect(
    host='localhost',
    port=pg_port,
    database=pg_db,
    user=pg_user,
    password=pg_password
)
cursor = conn.cursor()

print("Преобразование данных в текстовый буфер...")
output = io.StringIO()
df.to_csv(output, sep='\t', header=False, index=False)
output.seek(0)

print("Высокоскоростная вставка 10 млн строк в logs_pg...")
cursor.copy_from(output, 'logs_pg', sep='\t', columns=('user_id', 'timestamp', 'url', 'status_code'))
conn.commit()

cursor.close()
conn.close()
print("🎉 Все 10 миллионов строк успешно отправлены в PostgreSQL!")

