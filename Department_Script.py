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

def show_full_department_table():
    mycursor = connection.cursor()
    mycursor.execute("SELECT * FROM Department;")
    departments = mycursor.fetchall()
    print("Full Department Table:")
    for row in departments:
        print(row)
    mycursor.close()


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



show_full_department_table()

dept_id = int(input("Enter the department ID: "))
list_items(dept_id)

connection.close()
tunnel.stop()
