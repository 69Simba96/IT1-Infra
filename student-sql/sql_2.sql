CREATE TABLE logs_ch (
    user_id UInt64,
    timestamp DateTime,
    url String,
    status_code UInt16
) ENGINE = MergeTree()

SELECT user_id, count(*)
FROM logs_ch
WHERE timestamp > '2026-03-01 00:00:00'
GROUP BY user_id;

-- Время выполнения запроса: 0.136s
-- PG это время выполнения составляет 1.651s

DELETE FROM logs_ch WHERE user_id = 30505;

SELECT mutation_id, command, is_done
FROM system.mutations
WHERE table = 'logs_ch';


-- исходя из задания при удалении из клика должна была произойти ошибка, но у меня все нормально удадилось
-- в system.mutations
--mutation_11.txt	(UPDATE _row_exists = 0 WHERE user_id = 1)	1
--mutation_12.txt	(UPDATE _row_exists = 0 WHERE user_id = 30505)	1

-- часто так делать нельзя, потому что клик перезаписывает всю пачку и это приводит к сильной нагрузке на диски или процессор