import os
import datetime
import pandas as pd
import numpy as np
from clickhouse_connect import get_client

CH_USER = 'default'
CH_PASSWORD = 'password12345'

TOTAL_ROWS = 10000000
print(TOTAL_ROWS)

start_timestamp = int(datetime.datetime(2026, 1, 1).timestamp())
random_seconds = np.random.randint(0, 10000000, size=TOTAL_ROWS, dtype=np.int32)
timestamps = pd.to_datetime(start_timestamp + random_seconds, unit='s')

df = pd.DataFrame({
    'user_id': np.random.randint(1, 100000, size=TOTAL_ROWS, dtype=np.uint64),
    'timestamp': timestamps,
    'url': np.random.choice(['/home', '/cart', '/api', '/profile', '/payment'], size=TOTAL_ROWS),
    'status_code': np.random.choice([200, 201, 401, 403, 404, 500, 502, 503], size=TOTAL_ROWS).astype(np.uint16)
})


print("Подключение к ClickHouse")
client = get_client(host='localhost', port=8123, username=CH_USER, password=CH_PASSWORD)

client.insert_df('logs_ch', df)

print("Все успешно загружено")



