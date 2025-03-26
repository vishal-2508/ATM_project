import mysql.connector

class ConnectDatabase():
    def __init__(self,db_name=None):
        self.mydb = mysql.connector.connect(
          host="localhost",
          user="vishal",
          password="password",
          database=db_name
        )
class Bank:
    # create database
    def create_db(self,db_name,mycursor):
        string = "CREATE DATABASE " + db_name
        mycursor.execute(string)
    # create table
    def create_table(self,table_name,mycursor):
        string = ""
        if table_name == "bank_name":
            string = "CREATE TABLE " + table_name +  " (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))"
        elif table_name == "account_detail":
            string = "CREATE TABLE " + table_name +  " (id INT AUTO_INCREMENT PRIMARY KEY, account_no int not null UNIQUE, ifsc_code VARCHAR(10), balance int, bank_id int, user_id int, FOREIGN KEY (bank_id) REFERENCES bank_name(id), FOREIGN KEY (user_id) REFERENCES user_detail(id))"
        elif table_name == "user_detail":
            string = "CREATE TABLE " + table_name +  " (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(150),  address VARCHAR(300), mobile_no int)"
        else:
            print("Table is already create. ")
            return
        # print("final string is : ",string)
        mycursor.execute(string)
        
db = ConnectDatabase()
# connect database without batabase name
bank_operation = Bank()
mycursor = db.mydb.cursor()
mycursor.execute("SHOW DATABASES")
list_db = mycursor.fetchall()
db_name = input("Enter Database name : ")
# create database if database not exist
if (db_name,) not in list_db:
    check_db = input("database not exist do you want create new database Y or N : ")
    if check_db == 'Y' or check_db == 'y':
        bank_operation.create_db(db_name,mycursor)
mycursor.execute("SHOW DATABASES")
list_db = mycursor.fetchall()
# select database name
if (db_name,) in list_db:
    db = ConnectDatabase(db_name)
    # print("Add Database name : ",db.mydb)
    mycursor = db.mydb.cursor()
    check = 'Y'
    while check == "Y" or check == "y" :
        table_name = input("Enter table name : ")
        mycursor.execute("SHOW TABLES")
        list_table = mycursor.fetchall()
        # create table when not exist in databases
        if (table_name,) not in list_table:
            bank_operation.create_table(table_name,mycursor)
        check = input("Do you want to again add table Y or N : ")





