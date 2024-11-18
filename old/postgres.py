# pip install psycopg2
import psycopg2

try:
    # con = psycopg2.connect(user='postgres', password='123', host='127.0.0.1', port = '5432' ,database='Lib')
    con = psycopg2.connect(user='postgres', password='itI!1996', host='10.10.103.252', port='1912', database='Library')
    print(con)
    cursor = con.cursor()
    res = cursor.execute("select * from author;")
    result_set = cursor.fetchall()
    for record in result_set:
        print("Результат", record)
    con.close()
except:
    print("error")
