import pymysql.cursors


def to_connect():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='root',
                           db='ood',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)


def to_commit(connection):
    connection.commit()


def to_close(connection):
    connection.close()


def add_to_db(deal_id, user_id, text, indictment):
    # В sql запросе используется одинарная кавычка, поэтому избавляемся от неё в тексте
    if text.find("'") != -1:
        text = '"'.join(text.split("'"))

    connection = to_connect()
    try:
        with connection.cursor() as cursor:

            if indictment:
                check_row_sql = "SELECT * FROM indictment WHERE deal_id = {}" \
                    .format(deal_id)
                execute = cursor.execute(check_row_sql)
                if execute:
                    update_sql = "UPDATE indictment SET evidences = '{}' WHERE deal_id = {}"\
                        .format(text, deal_id)
                    cursor.execute(update_sql)
                else:
                    insert_sql = "INSERT INTO indictment (deal_id, evidences, established, justification) VALUES ({}, '{}', ' ', ' ')"\
                        .format(deal_id, text)
                    cursor.execute(insert_sql)
            else:

                sql = "INSERT INTO scans (deal_id, user_id, text) VALUES ({}, {}, '{}')" \
                    .format(deal_id, user_id, text)
                cursor.execute(sql)

            to_commit(connection)
    finally:
        to_close(connection)
