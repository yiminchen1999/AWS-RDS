import pymysql
import time
import asyncio
import aiomysql


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='cym991019',
                             database='ShapeMentor')

start_time = time.time()

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT * ,(SELECT SUM(value) FROM body_metrics WHERE user_id = u.user_id) as total_value, (SELECT SLEEP(1) AS delay) as delay FROM users u;")
        results = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT metric_index, metric_name, metric_unit, SLEEP(1) FROM body_metrics_lookup;")
        results = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute(
        "SELECT *,(SELECT SUM(value) FROM body_metrics WHERE user_id = u.user_id) as total_value,(SELECT COUNT(*) FROM body_metrics_lookup, (SELECT SLEEP(5) AS delay) AS a) as delay FROM users u;")
        results = cursor.fetchall()
        for result in results:
            print(result)
finally:
    connection.close()

end_time = time.time()
print("Synchronous call duration: {}".format(end_time - start_time))


async def async_query():
    conn = await aiomysql.connect(host='localhost', port=3306,
                                  user='root', password='cym991019',
                                  db='ShapeMentor')

    try:
        start_time = time.time()
        async with conn.cursor() as cursor:
            await cursor.execute(
                "SELECT * ,(SELECT SUM(value) FROM body_metrics WHERE user_id = u.user_id) as total_value, (SELECT SLEEP(1) AS delay) FROM users u;")
            results = await cursor.fetchall()

            await cursor.execute(
                "SELECT metric_index, metric_name, metric_unit, SLEEP(1) FROM body_metrics_lookup;")
            results = await cursor.fetchall()

            await cursor.execute(
                "SELECT *,(SELECT SUM(value) FROM body_metrics WHERE user_id = u.user_id) as total_value,(SELECT COUNT(*) FROM body_metrics_lookup, (SELECT SLEEP(5) AS delay) AS a) as delay FROM users u;")
            results = await cursor.fetchall()
            for result in results:
                print(result)
    finally:
        if conn is not None:
            conn.close()

    end_time = time.time()
    print("Asynchronous call duration: {}".format(end_time - start_time))

# Running the asynchronous loop
loop = asyncio.get_event_loop()
loop.run_until_complete(async_query())
