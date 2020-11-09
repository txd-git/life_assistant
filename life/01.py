import pymysql
db = pymysql.connect(host="localhost", port=3306, user="root", password="123456", database="Life_assistant", charset="utf8")
cur = db.cursor()

f = open("citys.txt", "r")  # 打开文件
for line in f:
    m = line.split('"')[1]
    n = line.split('"')[-2]
    try:
        sql = "insert into city (city_name,number) values (%s,%s);"
        cur.execute(sql, [m, n])
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
print('OK')