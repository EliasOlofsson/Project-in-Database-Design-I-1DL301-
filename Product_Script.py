from contextlib import closing
from os import getenv
import pymysql
from sshtunnel import SSHTunnelForwarder


def update_discount(conn, product_id):
    cur = conn.cursor()
    cur.execute(
        "SELECT Sale_percentage FROM Product "
        "WHERE Product_ID = %s",
        (product_id,)
    )
    current_discount = cur.fetchone()
    if current_discount:
        print(f"Current Discount: {current_discount[0]}")
        new_discount = float(input("Enter new discount: "))
        cur.execute(
            "UPDATE Product SET Sale_percentage = %s "
            "WHERE Product_ID = %s",
            (new_discount, product_id)
        )
        conn.commit()
        print("Discount updated")
    else:
        print("Product not found")
    cur.close()


with closing(
    SSHTunnelForwarder(
        ('fries.it.uu.se', 22),
        ssh_username=getenv("uu_username"),  # use your Studium username
        ssh_password=getenv("sqlpw"),  # use your Studium password
        remote_bind_address=('127.0.0.1', 3306)
    )
) as tunnel:
    tunnel.start()

    with closing(
        pymysql.connect(
            host='127.0.0.1',
            user='ht24_1_group_35',
            password='pasSWd_35',
            port=tunnel.local_bind_port,
            database='ht24_1_project_group_35'
        )
    ) as connection:
        id = 0
        while id != -1:
            id = int(input("Enter the product ID: "))
            update_discount(connection, id)
