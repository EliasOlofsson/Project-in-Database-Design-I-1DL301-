from contextlib import closing
from os import getenv
import pymysql
from sshtunnel import SSHTunnelForwarder


def list_items(conn, department_id):
    cur = conn.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM Department WHERE Parent_ID = %s",
        (department_id,)
    )
    if cur.fetchone()[0] == 0:
        cur.execute(
            (
                "SELECT Product_ID, Product_Title, "
                "(Price_without_VAT * (1 - Sale_percentage / 100)) "
                "FROM Product WHERE Department_ID = %s"
            ),
            (department_id,)
        )
        for row in cur.fetchall():
            print(row)
    else:
        cur.execute(
            (
                "SELECT Department_ID, Description "
                "FROM Department WHERE Parent_ID = %s"
            ),
            (department_id,)
        )
        for row in cur.fetchall():
            print(row)
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
            id = int(input("Enter the department ID: "))
            list_items(connection, id)
