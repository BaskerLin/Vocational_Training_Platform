# coding=utf8
import mysql.connector


my_db = mysql.connector.connect(
        host="localhost",  # 数据库主机地址
        user="root",  # 数据库用户名
        passwd="+0u(?9aOI%xi",  # 数据库密码
        database="database")

my_cursor = my_db.cursor()


def insert(table, header, value, num):
    sql_comment = "INSERT INTO" + " " + table + " " + header + " "
    value_num = "VALUES ("
    for i in range(num):
        if i != (num - 1):
            value_num += "%s, "
        else:
            value_num += "%s)"
    sql_comment = sql_comment + value_num

    print sql_comment
    print value
    my_cursor.execute(sql_comment, value)
    my_db.commit()
    # print(my_cursor.rowcount, "记录插入成功。")


def query_all(table):
    sql_comment = "SELECT * FROM " + table
    my_cursor.execute(sql_comment)
    result = my_cursor.fetchall()
    return result


def query_appoint_all_field(table, field):
    sql_comment = "SELECT "
    num = len(field)
    for i in range(num):
        if i != (num - 1):
            sql_comment += field[i] + ", "
        else:
            sql_comment += field[i] + " "
    sql_comment += sql_comment + "FROM " + table
    my_cursor.execute(sql_comment)
    result = my_cursor.fetchall()
    return result

