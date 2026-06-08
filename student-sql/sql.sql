CREATE TABLE web_logs (
     timestamp DateTime,
     user_id UInt64,
     url String,
     response_time UInt32,
     status_code UInt16
) ENGINE = MergeTree()
ORDER BY timestamp;

SELECT count() FROM web_logs;

-- запросы

SELECT toDate(timestamp) AS request_date, count(url) AS requests_count
FROM web_logs wl
GROUP BY request_date

SELECT url, avg(response_time) AS avg_time
FROM web_logs wl
GROUP BY url

SELECT count(url) AS request_count
FROM web_logs wl
WHERE toString(status_code) LIKE '4%' OR toString(status_code) LIKE '5%';

SELECT user_id, count(url) AS request_count
FROM web_logs wl
GROUP BY user_id
LIMIT 10