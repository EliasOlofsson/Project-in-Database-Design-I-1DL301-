import pymysql
from sshtunnel import SSHTunnelForwarder

tunnel = SSHTunnelForwarder(
    ('fries.it.uu.se', 22),
    ssh_username='Username',
    ssh_password='Password',
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

    # Insert sample data and update records
    insert_sample_data_sql = """
SET SQL_SAFE_UPDATES = 0;

INSERT INTO User_Emails (Email, IsVerified)
VALUES ('user1@example.com', 1), 
       ('user2@example.com', 0),
       ('user3@example.com', 1),
       ('user4@example.com', 0);

INSERT INTO User (Personal_ID_Number, Newsletter_permission, Name, Street_Name, Password, Street_Number, City, Postal_Code, Email_ID, PhoneNumber_ID)
VALUES 
('ABC123', 1, 'John Doe', 'Main St', 'password123', '10', 'New York', '10001', 1, NULL),
('XYZ789', 0, 'Jane Smith', 'Second St', 'password456', '20', 'Los Angeles', '90001', 2, NULL),
('DEF456', 1, 'Mike Johnson', 'Third St', 'password789', '30', 'Chicago', '60601', 3, NULL),
('GHI012', 0, 'Emily Davis', 'Fourth St', 'password012', '40', 'Houston', '77001', 4, NULL);

INSERT INTO User_PhoneNumbers (PhoneNumber, IsVerified, User_ID)
VALUES 
('1234567890', 1, 1), 
('0987654321', 0, 2),
('1112223333', 1, 3),
('2223334444', 0, 4);

UPDATE User
SET PhoneNumber_ID = (
    SELECT PhoneNumber_ID 
    FROM User_PhoneNumbers 
    WHERE User_PhoneNumbers.User_ID = User.User_ID
)
WHERE User.User_ID IS NOT NULL;

INSERT INTO Department (Department_ID, Description, Parent_ID)
VALUES 
(1, 'Electronics', NULL), 
(2, 'Computers and Tablets', 1),
(3, 'Desktops', 2),
(4, 'Laptops', 2),
(5, 'Tablets', 2),
(6, 'Accessories', 2),
(7, 'For Desktops', 6),
(8, 'For Laptops', 6),
(9, 'For Tablets', 6),
(10, 'TV and Video', 1),
(11, 'TVs', 10),
(12, 'Projectors', 10);

INSERT INTO Product (Product_Title, Description, Price_without_VAT, Stock_qty, VAT_percentage, Sale_percentage, AVG_Rating)
VALUES 
('iPhone 13', 'Latest Apple iPhone with advanced features', 799.00, 25, 10.00, 5.00, 4.8),
('Samsung Galaxy S21', 'Flagship Samsung smartphone with great camera', 699.00, 30, 10.00, 10.00, 4.5),
('Dell XPS 13', 'Compact and powerful laptop with 13-inch display', 999.00, 15, 12.00, 8.00, 4.7),
('Sony Bravia 55"', 'High-resolution 55-inch TV with smart features', 1199.00, 10, 15.00, 20.00, 4.6),
('Philips Air Fryer', 'Healthier frying with minimal oil usage', 199.00, 60, 10.00, 7.00, 4.7),
('LG Desktop', 'High-performance desktop for office and gaming', 999.00, 20, 12.00, 5.00, 4.3),
('Apple iPad Pro', 'Apple iPad Pro with M1 chip', 1099.00, 15, 10.00, 8.00, 4.9),
('Bose Home Speaker 500', 'High-quality home speaker with voice assistant', 349.00, 30, 10.00, 10.00, 4.6),
('Epson Projector', '4K projector with bright resolution', 849.00, 12, 15.00, 8.00, 4.5),
('Samsung 75" TV', '75-inch smart TV with 4K UHD display', 1499.00, 8, 10.00, 5.00, 4.9);

INSERT INTO Department (Description, Product_ID, Parent_ID)
VALUES 
('Desktops', 6, 3),
('Laptops', 3, 4),
('Tablets', 7, 5),
('TVs', 10, 11),
('Projectors', 9, 12);

INSERT INTO Review (Stars, Text, Product_ID, User_ID)
VALUES 
(5, 'Amazing product, highly recommend it!', 1, 1),
(4, 'Good value for money, satisfied with the purchase.', 1, 2),
(5, 'Excellent sound quality, worth every penny.', 8, 3),
(3, 'Decent product, could be cheaper.', 4, 4),
(5, 'Best TV I have ever owned!', 10, 2),
(4, 'The projector works well, but needs better brightness.', 9, 1);

INSERT INTO `Order` (Date, Status, Last_Change, Tracking_nr, Payment_ref, Cost, User_ID)
VALUES 
('2023-09-01', 'Processing', '2023-09-01', 'TRK123', 'PAY123', 150.00, 1),
('2023-09-02', 'Shipped', '2023-09-02', 'TRK456', 'PAY456', 250.00, 2),
('2023-09-03', 'Delivered', '2023-09-03', 'TRK789', 'PAY789', 300.00, 3);

INSERT INTO Ordered_Product (Quantity, Order_ID, Product_ID)
VALUES 
(2, 1, 1), 
(1, 2, 2), 
(3, 3, 8);

INSERT INTO Product_Info (Cost, Product_Name_At_Purchase, Product_ID)
VALUES 
(799.00, 'iPhone 13', 1), 
(699.00, 'Samsung Galaxy S21', 2), 
(999.00, 'Dell XPS 13', 3), 
(1199.00, 'Sony Bravia 55"', 4), 
(199.00, 'Philips Air Fryer', 5), 
(999.00, 'LG Desktop', 6), 
(1099.00, 'Apple iPad Pro', 7), 
(349.00, 'Bose Home Speaker 500', 8), 
(849.00, 'Epson Projector', 9), 
(1499.00, 'Samsung 75" TV', 10);

INSERT INTO Keyword (`Key`, Product_ID)
VALUES 
('smartphone', 1),
('smartphone', 2),
('laptop', 3),
('TV', 4),
('air fryer', 5),
('desktop', 6),
('tablet', 7),
('speaker', 8),
('projector', 9),
('TV', 10);

SET SQL_SAFE_UPDATES = 1;
"""


    for sql_statement in insert_sample_data_sql.split(';'):
        if sql_statement.strip():
            mycursor.execute(sql_statement)

    mydb.commit()
    print("Sample data inserted and updated successfully.")

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
