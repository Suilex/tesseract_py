import pymysql.cursors


def to_connect():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='',
                           db='oodt',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)


def to_commit(connection):
    connection.commit()


def to_close(connection):
    connection.close()


def add_to_db(deal_id, user_id, text):
    # В sql запросе используется одинарная кавычка, поэтому избавляемся от неё в тексте
    if text.find("'") != -1:
        text = '"'.join(text.split("'"))

    connection = to_connect()
    try:
        with connection.cursor() as cursor:

            sql = "INSERT INTO scans (deal_id, user_id, text) VALUES ({}, {}, '{}')" \
                .format(deal_id, user_id, text)

            cursor.execute(sql)
            to_commit(connection)
    finally:
        to_close(connection)
