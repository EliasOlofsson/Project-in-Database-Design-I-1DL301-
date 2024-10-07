import pymysql
from sshtunnel import SSHTunnelForwarder

tunnel = SSHTunnelForwarder(
    ('fries.it.uu.se', 22),
    ssh_username='USERNAME',
    ssh_password='PASSWORD',
    remote_bind_address=('127.0.0.1', 3306)
)
tunnel.start()

connection = pymysql.connect(
    host='127.0.0.1',
    user='ht24_1_group_35',
    password='pasSWd_35',
    port=tunnel.local_bind_port,
    database='ht24_1_project_group_35'
)

def list_items(department_id):
    cur = connection.cursor()
    cur.execute("SELECT COUNT(*) FROM Department WHERE Parent_ID = %s", (department_id,))
    if cur.fetchone()[0] == 0:
        cur.execute("SELECT Product_ID, Product_Title, (Price_without_VAT * (1 - Sale_percentage / 100)) FROM Product WHERE Department_ID = %s", (department_id,))
        for row in cur.fetchall():
            print(row)
    else:
        cur.execute("SELECT Department_ID, Description FROM Department WHERE Parent_ID = %s", (department_id,))
        for row in cur.fetchall():
            print(row)
    cur.close()

list_items(int(input("Enter the department ID: ")))

connection.close()
tunnel.stop()
