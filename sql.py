import pymysql

# Replace the following with your own details
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='cym991019',
                             database='ShapeMentor')

try:
  # Execute a query
  with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM body_metrics_lookup")
    results = cursor.fetchall()
    for result in results:
      print(result)

    pass
finally:
  connection.close()
  print("Connection closed.")
