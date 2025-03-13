from connect_to_base import conn_base


def analysis_table(cur) -> None:
    """Table analysis"""

    """ Сколько записей (строк) хранится в каждой таблице? """
    for name in range(1, 4):
        cur.execute(f"""SELECT COUNT(*) FROM table_{name}""")
        counter = cursor.fetchone()[0]
        print(f"table_{name} has {counter} rows")

    """ Сколько в таблице table_1 уникальных записей? """
    cur.execute("""SELECT COUNT(DISTINCT value) FROM table_1""")
    result = cursor.fetchone()[0]
    print(f"\ntable_1 has '{result}' unique records")

    """ Как много записей из таблицы table_1 встречается в table_2 """
    cur.execute("""SELECT COUNT(*) FROM table_1 JOIN table_2 ON table_1.id = table_2.id""")
    result = cursor.fetchone()[0]
    print(f"\nfrom table_1 is found in table_2 '{result}' records")

    """ Как много записей из таблицы table_1 встречается и в table_2, и в table_3? """
    cur.execute(
        """SELECT COUNT(*) FROM table_1 t1 JOIN table_2 t2 ON t1.id = t2.id JOIN table_3 t3 on t1.value = t3.value"""
    )
    result = cursor.fetchone()[0]
    print(f"\nfrom table_1, it occurs in both table_2 and table_3 '{result}' records")


if __name__ == '__main__':
    cursor = conn_base('hw_3_database.db')
    analysis_table(cursor)
