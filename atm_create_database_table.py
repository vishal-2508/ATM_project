import mysql.connector

class ConnectDatabase():
    '''
    this class is connect to python mysql with database.
    '''
    def __init__(self,db_name=None):
        self.mydb = mysql.connector.connect(
          host="localhost",
          user="vishal",
          password="password",
          database=db_name
        )
class Bank:
    """
    Generally this class is create database and table if not exist.
    """
    def create_db(self,db_name,mycursor):
        """
        create new database.
        Args:
            db_name (str): name of database
            mycursor (class): pointer of mysql corsor
        """
        string = f"CREATE DATABASE {db_name}"
        mycursor.execute(string)
        print(f"{db_name} database is Successfully create. ")
        
    def create_table(self,table_name,mycursor):
        """
        create new table.
        Args:
            table_name (str): name of table
            mycursor (class): pointer of mysql corsor
        """
        string = ""
        if table_name == "bank_name":
            string = f"CREATE TABLE {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(6))"
        elif table_name == "account_detail":
            string = f"CREATE TABLE {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, account_no int not null UNIQUE, ifsc_code VARCHAR(6), balance int, bank_id int, user_id int, FOREIGN KEY (bank_id) REFERENCES bank_name(id), FOREIGN KEY (user_id) REFERENCES user_detail(id))"
        elif table_name == "user_detail":
            string = f"CREATE TABLE {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(20),  address VARCHAR(50), mobile_no int)"
        else:
            print("Table is already create. ")
            return
        mycursor.execute(string)
        print(f"{table_name} table is Successfully create.")

try:
    # connect database without batabase name   
    # fetch all databases name in list_db_name in list format.
    db = ConnectDatabase()
    mycursor = db.mydb.cursor()
    mycursor.execute("SHOW DATABASES")
    list_db_name = mycursor.fetchall()
    # create Bank class object.
    # create database if database not exist
    bank_operation = Bank()
    db_name = input("Enter Database name : ")
    if (db_name,) not in list_db_name:
        check_condition = input(f"{db_name} database is not exist do you want create new database y or n : ")  
        if check_condition.lower() == 'y' :
            bank_operation.create_db(db_name,mycursor)
    mycursor.execute("SHOW DATABASES")
    list_db_name = mycursor.fetchall()
    # check db name exist in list of database name.
    if (db_name,) in list_db_name:
        # connect database with batabase name.
        db = ConnectDatabase(db_name)
        mycursor = db.mydb.cursor()
        check_condition = 'y'
        while check_condition.lower() == "y":
            table_name = input("create first parant table after that child table \nEnter table name : ")
            mycursor.execute("SHOW TABLES")
            list_table = mycursor.fetchall()
            # create table when not exist in databases
            if (table_name,) not in list_table:
                bank_operation.create_table(table_name,mycursor)
            check_condition = input("Do you want to again add table y or n : ")
        # Insert bank name like BOB, SBI, YES
        if input("Do you want to add bank name y or n : ").lower() == 'y':
            bank_name = [('BOB',),('SBI',),('YES',)]
            for name in bank_name:
                sql = "INSERT INTO bank_name (name) VALUES (%s)"
                mycursor.execute(sql, name)
                db.mydb.commit()
            print("bank name insert Successfully")
    
except Exception as e:
    print("Exception as e...",e)


