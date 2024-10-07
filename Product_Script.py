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

def update_discount(product_id):
    cur = connection.cursor()
    cur.execute("SELECT Sale_percentage FROM Product WHERE Product_ID = %s", (product_id,))
    current_discount = cur.fetchone()
    if current_discount:
        print(f"Current Discount: {current_discount[0]}")
        new_discount = float(input("Enter new discount: "))
        cur.execute("UPDATE Product SET Sale_percentage = %s WHERE Product_ID = %s", (new_discount, product_id))
        connection.commit()
        print("Discount updated")
    else:
        print("Product not found")
    cur.close()

update_discount(int(input("Enter the product ID: ")))

connection.close()
tunnel.stop()
