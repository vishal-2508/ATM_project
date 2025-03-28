import mysql.connector
import random
import string

class ConnectDatabase():
    '''
    this class is connect to python mysql with database.
    ''' 
    def __init__(self):
        self.mydb = mysql.connector.connect(
          host="localhost",
          user="vishal",
          password="password",
          database="atm"
        )

class Bank:
    """
    group of all banking features. like bank name, create and login account etc.
    """
    def __init__(self):
        self.db = ConnectDatabase()
        self.mycursor = self.db.mydb.cursor()
        self.right = True
    
    def withdraw_credit_balance(self,account_no,login_account_data):
        '''
        it's perform operation like credit money, withdraw money, show balance, show customer detail etc.
        Args:
            account_no (int): user account no.
            login_account_data (dict): costumer account detail.
        '''
        print(f"Account no : {account_no} \nIFSC Code : {login_account_data[account_no]['ifsc_code']} \ncustomer Name : {login_account_data[account_no]['name']}" )
        while self.right:
            number = int(input("1. Credit money \n2. Withdraw money \n3. Show balance \n4. Show account detail \n5. Back \n6. Exit \nPress key : "))        
            # Credit money
            if number == 1:
                add_balance = int(input("Enter amount : "))
                login_account_data[account_no]['balance'] += add_balance
                print("Successfully credit amount in your account.")
            # Withdraw money
            elif number == 2:
                withdraw_money =  int(input("Enter withdrawal amount : "))
                if login_account_data[account_no]['balance'] >= withdraw_money:
                    login_account_data[account_no]['balance'] -= withdraw_money
                    print("Successfully withdrawal balance in your account.")
                else:
                    print(f"Sorry insufficient balance in account. only you can withdraw equal or more then {login_account_data[account_no]['balance']} " )
            # Show balance
            elif number == 3:
                print(f"Total balance : {login_account_data[account_no]['balance']}" )
            # Show account detail
            elif number == 4:
                print(f"Account no : {account_no} \nIFSC Code : {login_account_data[account_no]['ifsc_code']} \nCustomer Name : {login_account_data[account_no]['name']} \nAddress : {login_account_data[account_no]['address']} \nMobile no : {login_account_data[account_no]['mobile_no']}" )
            # Back
            elif number == 5:
                break
            # Exit
            elif number == 6:
                self.right = False
            else:
                print("Please enter valid key... ")
        sql = f"UPDATE account_detail SET balance = {login_account_data[account_no]['balance']} WHERE account_no = {(account_no)}"
        self.mycursor.execute(sql)
        self.db.mydb.commit()
    
    def create_account(self,bank_id,user_data):
        """ 
        create new customer account.
        Args:
            bank_id (int): select bank id
            user_data (dict): user account detail
        """
        # insert data in user_detail table
        data = list(input("Enter name, address, mobile no with comma separet : ").strip().split(","))
        sql = "INSERT INTO user_detail (name, address, mobile_no) VALUES (%s, %s, %s)"
        val = (data[0], data[1], data[2])
        self.mycursor.execute(sql, val)
        self.db.mydb.commit()
        # fetch last insert rocord id from user_detail table 
        self.mycursor.execute("SELECT LAST_INSERT_ID()")
        user_id_list = self.mycursor.fetchall()
        # insert data in account_detail table
        # create random account no and ifsc code
        account_no = random.randint(10000, 99999)
        while account_no in user_data:
            account_no = random.randint(10000, 99999)
        length = 6  
        characters = string.ascii_uppercase + string.digits
        ifsc_code = ''.join(random.choices(characters, k=length))
        sql = "INSERT INTO account_detail (account_no, ifsc_code, balance, bank_id, user_id) VALUES (%s, %s, %s, %s, %s)"
        val = (account_no, ifsc_code, 0, bank_id, user_id_list[0][0] )
        self.mycursor.execute(sql, val)
        self.db.mydb.commit()
        # fetch last insert rocord id from account_detail table
        self.mycursor.execute("SELECT LAST_INSERT_ID()")
        parant_id_list = self.mycursor.fetchall()
        # add created account detail in user data
        user_data[account_no] = {'parant_id':parant_id_list[0][0], 'ifsc_code':ifsc_code, 'balance':0, 'bank_id':bank_id, 'user_id':user_id_list[0][0], 'child_id':user_id_list[0][0], 'name':data[0], 'address':data[1], 'mobile_no':data[2] }
        print("Your account is successfully create... ")
        print(f"Account no : {account_no} \nIFSC Code : {ifsc_code} \nCustomer Name : {data[0]} \nAddress : {data[1]} \nMobile no : {data[2]} " )

    def find_bank_account(self,bank_id,bank_data,user_data):
        """
        this is allows a user to create or login account in existing bank bank.
        Args:
            bank_id (int): select bank id.
            bank_data (dict): Bank name detail .
            user_data (dict): user account detail.
        """
        while self.right:
            number = int(input("1. Create account \n2. Login account \n3. Back \n4. Exit \npress key : "))
            # Create account
            if number == 1:
                self.create_account(bank_id,user_data)
            # Login account
            elif number == 2:
                while True:
                    account_no = int(input("1. Back \nEnter account no : "))
                    if account_no == 1 :
                        break
                    elif account_no in user_data:
                        login_account_data = {}
                        login_account_data[account_no] = user_data[account_no]
                        self.withdraw_credit_balance(account_no,login_account_data)
                        break
                    else:
                        print("Please enter right account no. ")
            # Back
            elif number == 3:
                break
            # Exit
            elif number == 4:
                self.right = False
            else:
                print("Please enter valid key. ")            

    def all_bank(self):
        """
        this is show all bank name from bank_name table.
        """
        self.mycursor.execute("SELECT * FROM bank_name")
        bank_name_list = self.mycursor.fetchall()
        while self.right:
            bank_data = {}
            for id_name in bank_name_list:
                print(id_name[0], ":", id_name[1])
                bank_data[id_name[0]] = id_name[1]
            print( (bank_name_list[-1][0]+1), ": Exit" )
            bank_id = int(input("choose bank name : "))
            # check bank_id exit in bank_data dictionary.
            if bank_id in bank_data:
                self.mycursor.execute(f"select * from account_detail as ad inner join user_detail as ud on ad.bank_id = {bank_id} and ad.user_id = ud.id ")
                # fetch specific bank customer data in account_list.
                # account_list data convert into user_data dictionary.
                account_list = self.mycursor.fetchall()
                user_data = { data[1] : {"parant_id":data[0], "ifsc_code":data[2], "balance":data[3], "bank_id":data[4], "user_id":data[5], "child_id":data[6], "name":data[7], "address":data[8], "mobile_no":data[9] } for data in account_list}
                self.find_bank_account(bank_id,bank_data,user_data)
            # Exit
            elif bank_id == (bank_name_list[-1][0]+1):
                break
            # more then bank_id to display of key.
            else:
                print("Please enter valid number : ")

try:
    atm_features = Bank()
    atm_features.all_bank()
except Exception as e:
    print("Exception as e..... ",e)