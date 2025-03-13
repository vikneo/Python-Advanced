from email.mime import base
import os
import sqlite3

BASE_DIR = os.path.dirname(__file__)
base_name = 'hw.db'
path_to_db = os.path.join(BASE_DIR, base_name)


sql_select_1 = """
    SELECT c.full_name, m.full_name, purchase_amount, date FROM "order" as o
    INNER JOIN customer as c ON c.customer_id = o.customer_id
    INNER JOIN manager as m ON m.manager_id = o.manager_id
"""

sql_select_2 = """
    SELECT full_name FROM customer
    LEFT JOIN "order" as o ON o.customer_id = customer.customer_id
    WHERE o.customer_id is NULL
    ORDER BY full_name
"""

sql_select_3 = """
    SELECT o.order_no, c.full_name, m.full_name FROM "order" as o
    JOIN customer as c ON c.customer_id = o.customer_id
    JOIN manager as m ON m.manager_id = o.manager_id
    WHERE c.city <> m.city
"""

sql_select_4 = """
    SELECT c.full_name, o.order_no FROM "order" as o
    JOIN customer as c ON c.customer_id = o.customer_id
    WHERE o.manager_id IS NULL
"""

sql_select_5 = """
    SELECT c1.full_name as customer_1,  c2.full_name as customer_2
    FROM customer as c1
    JOIN customer as c2 ON c1.customer_id != c2.customer_id
    WHERE c1.city = c2.city AND c1.manager_id = c2.manager_id
"""


def main():
    with sqlite3.connect(path_to_db) as connect:
        cursor = connect.cursor()
        orders = cursor.execute(sql_select_1).fetchall()
        not_orders = cursor.execute(sql_select_2).fetchall()
        customer_not_in_city_manager = cursor.execute(sql_select_3).fetchall()
        print(f"Общее кол-во заказов - ({len(orders)}) шт.")
        print(f"Кол-во покупателей, которые не делали заказов - ({len(not_orders)}) шт.")
        print(f"Кол-во заказов, где покупатель не живет в городе продавца - ({len(customer_not_in_city_manager)}) шт.")

if __name__ == '__main__':
    main()
