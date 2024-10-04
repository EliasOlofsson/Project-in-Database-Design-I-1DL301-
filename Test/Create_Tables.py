import pymysql
from sshtunnel import SSHTunnelForwarder

tunnel = SSHTunnelForwarder(
    ('fries.it.uu.se', 22),
    ssh_username='Anv',
    ssh_password='Pass',
    remote_bind_address=('127.0.0.1', 3306)
)

try:
    tunnel.start()
    mydb = pymysql.connect(
        host='127.0.0.1',
        user='ht24_1_group_35',
        password='pasSWd_35',
        port=tunnel.local_bind_port,
        db='ht24_1_project_group_35'
    )

    mycursor = mydb.cursor()

    create_tables_sql = """
    CREATE TABLE User_Emails (
        Email_ID INT AUTO_INCREMENT PRIMARY KEY,
        Email VARCHAR(255) UNIQUE,
        IsVerified BOOLEAN DEFAULT 0
    );

    CREATE TABLE User (
        User_ID INT AUTO_INCREMENT PRIMARY KEY,
        Personal_ID_Number VARCHAR(50) UNIQUE,
        Newsletter_permission BOOLEAN DEFAULT 0,
        Name VARCHAR(100),
        Street_Name VARCHAR(100),
        Password VARCHAR(255),
        Street_Number VARCHAR(10),
        City VARCHAR(50),
        Postal_Code VARCHAR(20),
        Email_ID INT,
        PhoneNumber_ID INT
    );

    CREATE TABLE User_PhoneNumbers (
        PhoneNumber_ID INT AUTO_INCREMENT PRIMARY KEY,
        PhoneNumber VARCHAR(20),
        IsVerified BOOLEAN DEFAULT 0,
        User_ID INT
    );

    CREATE TABLE Product (
        Product_ID INT AUTO_INCREMENT PRIMARY KEY,
        Product_Title VARCHAR(255),
        Description TEXT,
        Price_without_VAT DECIMAL(10, 2),
        Stock_qty INT,
        VAT_percentage DECIMAL(5, 2),
        Sale_percentage DECIMAL(5, 2),
        AVG_Rating DECIMAL(3, 2)
    );

    CREATE TABLE Department (
        Department_ID INT AUTO_INCREMENT PRIMARY KEY,
        Description TEXT,
        Product_ID INT
    );

    CREATE TABLE Product_Info (
        Product_Info_ID INT AUTO_INCREMENT PRIMARY KEY,
        Cost DECIMAL(10, 2),
        Product_Name_At_Purchase VARCHAR(255),
        Product_ID INT
    );

    CREATE TABLE Keyword (
        Key_ID INT AUTO_INCREMENT PRIMARY KEY,
        `Key` VARCHAR(100),
        Product_ID INT
    );

    CREATE TABLE Review (
        Review_ID INT AUTO_INCREMENT PRIMARY KEY,
        Stars INT CHECK (Stars BETWEEN 1 AND 5),
        Text TEXT,
        Product_ID INT,
        User_ID INT
    );

    CREATE TABLE `Order` (
        Order_ID INT AUTO_INCREMENT PRIMARY KEY,
        Date DATE,
        Status VARCHAR(50),
        Last_Change DATE,
        Tracking_nr VARCHAR(100),
        Payment_ref VARCHAR(100),
        Cost DECIMAL(10, 2),
        User_ID INT
    );

    CREATE TABLE Ordered_Product (
        Ordered_Product_ID INT AUTO_INCREMENT PRIMARY KEY,
        Quantity INT,
        Order_ID INT,
        Product_ID INT
    );

    CREATE TABLE Makes_a (
        User_ID INT,
        Review_ID INT,
        PRIMARY KEY (User_ID, Review_ID)
    );

    ALTER TABLE User
    ADD CONSTRAINT fk_user_email FOREIGN KEY (Email_ID) REFERENCES User_Emails(Email_ID);

    ALTER TABLE User_PhoneNumbers
    ADD CONSTRAINT fk_user_phonenumbers_user FOREIGN KEY (User_ID) REFERENCES User(User_ID);

    ALTER TABLE User
    ADD CONSTRAINT fk_user_phonenumber FOREIGN KEY (PhoneNumber_ID) REFERENCES User_PhoneNumbers(PhoneNumber_ID);

    ALTER TABLE Department
    ADD CONSTRAINT fk_department_product FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID);

    ALTER TABLE Product_Info
    ADD CONSTRAINT fk_productinfo_product FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID);

    ALTER TABLE Keyword
    ADD CONSTRAINT fk_keyword_product FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID);

    ALTER TABLE Review
    ADD CONSTRAINT fk_review_product FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID),
    ADD CONSTRAINT fk_review_user FOREIGN KEY (User_ID) REFERENCES User(User_ID);

    ALTER TABLE `Order`
    ADD CONSTRAINT fk_order_user FOREIGN KEY (User_ID) REFERENCES User(User_ID);

    ALTER TABLE Ordered_Product
    ADD CONSTRAINT fk_orderedproduct_order FOREIGN KEY (Order_ID) REFERENCES `Order`(Order_ID),
    ADD CONSTRAINT fk_orderedproduct_product FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID);

    ALTER TABLE Makes_a
    ADD CONSTRAINT fk_makesa_user FOREIGN KEY (User_ID) REFERENCES User(User_ID),
    ADD CONSTRAINT fk_makesa_review FOREIGN KEY (Review_ID) REFERENCES Review(Review_ID);
    """

    for sql_statement in create_tables_sql.split(';'):
        if sql_statement.strip():
            mycursor.execute(sql_statement)
    
    mydb.commit()

    mycursor.execute("SHOW TABLES")
    for x in mycursor:
        print(x)

finally:
    if mycursor:
        mycursor.close()
    if mydb.open:
        mydb.close()
    if tunnel.is_active:
        tunnel.stop()
