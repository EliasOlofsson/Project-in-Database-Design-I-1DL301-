import pymysql
from sshtunnel import SSHTunnelForwarder

tunnel = SSHTunnelForwarder( # Connecting via SSH as per template
    ('fries.it.uu.se', 22),
    ssh_username='USERNAME',
    ssh_password='PASSWORD',
    remote_bind_address=('127.0.0.1', 3306)
)
tunnel.start()

connection = pymysql.connect( #Connecting to database
    host='127.0.0.1',
    user='ht24_1_group_35',
    password='pasSWd_35',
    port=tunnel.local_bind_port,
    database='ht24_1_project_group_35'
)

def show_full_department_table(): # This function is used to display the department table
    cursor = connection.cursor() # By executing a SQL Query and iterating throu the response to append to a list
    cursor.execute("SELECT * FROM Department;")
    departments = cursor.fetchall()
    print("Full Department Table:")
    for row in departments:
        print(row)
    cursor.close()

def show_full_product_table(): # This function is used to display the product table
    cursor = connection.cursor() # By usexecuting a SQL Query and iterating throu the response to append to a list
    cursor.execute("SELECT Product_ID, Product_Title, Sale_percentage FROM Product;")
    products = cursor.fetchall()
    print("Product ID, Name and Sale Percentage:")
    for row in products: # Simple append for the right data, not neccicary to display full table
        print(f"Product ID: {row[0]}, Product: {row[1]}, Sale: {row[2]}%")
    cursor.close()

def list_items(): # This is the function for listing child departments for non-leaf nodes
    show_full_department_table() # Show department table function
    dept_id = int(input("Enter the department ID: ")) # User input
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM Department WHERE Parent_ID = %s", (dept_id,))
    child_count = cursor.fetchone()[0] # Check for first value
    if child_count == 0: # If empty its leaf node
        cursor.execute(
            "SELECT Product_ID, Product_Title, (Price_without_VAT * (1 - Sale_percentage / 100)) "
            "FROM Product WHERE Department_ID = %s", (dept_id,)
        )
        print("Products in the department:")
        for row in cursor.fetchall():
            print(f"Product ID: {row[0]}, Product Title: {row[1]}, Discounted Price: {row[2]}")
    else: # Else list child departments
        cursor.execute(
            "SELECT Department_ID, Description FROM Department WHERE Parent_ID = %s", (dept_id,)
        )
        print("Sub-departments:")
        for row in cursor.fetchall():
            print(f"Department ID: {row[0]}, Description: {row[1]}")
    cursor.close()

def update_discount(): # Function for updating sale %
    show_full_product_table() # Show table product table function
    product_id = int(input("Enter the product ID to update discount: "))
    cursor = connection.cursor()
    cursor.execute("SELECT Sale_percentage FROM Product WHERE Product_ID = %s", (product_id,))
    current_discount = cursor.fetchone()
    if current_discount is not None: # Just checking so there is a product with the inputed id
        print(f"Current Discount: {current_discount[0]}") # Display discount
        new_discount = float(input("Enter new discount: ")) # Input a new discount as float
        cursor.execute("UPDATE Product SET Sale_percentage = %s WHERE Product_ID = %s", (new_discount, product_id))
        connection.commit() # Send the update Query
        print("Discount updated")
    else: # Just to close the func if not found
        print("Product not found")
    cursor.close()

def main_menu(): # This is the combined part for choosing operation
    print("Choose an operation:")
    print("1. List items or sub-departments")
    print("2. Update a product discount")
    choice = input("Enter 1 or 2: ")
    if choice == "1": # Simple if else for selected input
        list_items()
    elif choice == "2":
        update_discount()
    else: # Just in case of a missinput
        print("Invalid choice, please enter 1 or 2.")

main_menu() # Run the first function 

connection.close() # Close database connection  
tunnel.stop() # Close tunnel to free space
