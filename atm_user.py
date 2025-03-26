import mysql.connector
import random
import string

class ConnectDatabase():
    def __init__(self):
        self.mydb = mysql.connector.connect(
          host="localhost",
          user="vishal",
          password="password",
          database="atm"
        )

class Bank:
    def __init__(self):
        self.db = ConnectDatabase()
        self.mycursor = self.db.mydb.cursor()
        self.right = True

    # Withdraw and credit amount from bank
    def withdraw_credit_balance(self,account_no,login_account_data):
        # print(login_account_data)
        print("Account no : ",account_no, "\nIFSC Code : ", login_account_data[account_no]["ifsc_code"], "\ncustomer Name : ", login_account_data[account_no]["name"] )
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
                    print("Sorry insufficient balance in account. only you can withdraw equal or more then ", login_account_data[account_no]['balance'] )
            # Show balance
            elif number == 3:
                print("Total balance : ", login_account_data[account_no]['balance'])
            # Show account detail
            elif number == 4:
                print("Account no : ",account_no, "\nIFSC Code : ", login_account_data[account_no]["ifsc_code"], "\nCustomer Name : ", login_account_data[account_no]["name"], "\nAddress : ", login_account_data[account_no]["address"], "\nMobile no : ", login_account_data[account_no]["mobile_no"] )
            # Back
            elif number == 5:
                break
            # Exit
            elif number == 6:
                self.right = False
            else:
                print("Please enter valid key... ")
        sql = "UPDATE account_detail SET balance = "+ str(login_account_data[account_no]['balance']) +" WHERE account_no = " + str(account_no)
        self.mycursor.execute(sql)
        self.db.mydb.commit()

    # create account
    def create_account(self,choose,bank_data,user_data):
        # insert data in user_detail table
        data = list(input("Enter name, address, mobile no with comma separet : ").strip().split(","))
        sql = "INSERT INTO user_detail (name, address, mobile_no) VALUES (%s, %s, %s)"
        val = (data[0], data[1], data[2])
        self.mycursor.execute(sql, val)
        self.db.mydb.commit()
        # fetch last insert rocord id in user_detail table 
        self.mycursor.execute("SELECT LAST_INSERT_ID()")
        user_id = self.mycursor.fetchall()
        # insert data in account_detail table
        # create random account no and ifsc code
        account_no = random.randint(10000, 99999)
        while account_no in user_data:
            account_no = random.randint(10000, 99999)
        length = 6  
        characters = string.ascii_uppercase + string.digits
        ifsc_code = ''.join(random.choices(characters, k=length))
        sql = "INSERT INTO account_detail (account_no, ifsc_code, balance, bank_id, user_id) VALUES (%s, %s, %s, %s, %s)"
        val = (account_no, ifsc_code, 0, choose, user_id[0][0] )
        self.mycursor.execute(sql, val)
        self.db.mydb.commit()
        # fetch last insert rocord id in account_detail table
        self.mycursor.execute("SELECT LAST_INSERT_ID()")
        parant_id = self.mycursor.fetchall()
        # add created account detail in user data
        user_data[account_no] = {'parant_id':parant_id, 'ifsc_code':ifsc_code, 'balance':0, 'bank_id':choose, 'user_id':user_id[0][0], 'child_id':user_id[0][0], 'name':data[0], 'address':data[1], 'mobile_no':data[2] }
        print("Your account is successfully create... ")
        print("Account no : ",account_no, "\nIFSC Code : ", ifsc_code, "\nCustomer Name : ", data[0], "\nAddress : ", data[1], "\nMobile no : ", data[2] )

    # Create account and login account
    def find_bank_account(self,choose,bank_data,user_data):
        while self.right:
            number = int(input("1. Create account \n2. Login account \n3. Back \n4. Exit \npress key : "))
            # Create account
            if number == 1:
                self.create_account(choose,bank_data,user_data)
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

    # show all bank name 
    def all_bank(self):
        self.mycursor.execute("SELECT * FROM bank_name")
        myresult = self.mycursor.fetchall()
        while self.right:
            bank_data = {}
            for i in myresult:
                print(i[0], ":", i[1])
                bank_data[i[0]] = i[1]
            print( (myresult[-1][0]+1), ": Exit" )
            choose = int(input("choose bank name : "))
            if choose in bank_data:
                self.mycursor.execute("select * from account_detail as ad inner join user_detail as ud on ad.bank_id = "+ str(choose) +" and ad.user_id = ud.id ")
                myaccount = self.mycursor.fetchall()
                # print("myaccount : ", myaccount)
                user_data = { i[1] : {"parant_id":i[0], "ifsc_code":i[2], "balance":i[3], "bank_id":i[4], "user_id":i[5], "child_id":i[6], "name":i[7], "address":i[8], "mobile_no":i[9] } for i in myaccount}
                self.find_bank_account(choose,bank_data,user_data)
            elif choose == (myresult[-1][0]+1):
                break
            else:
                print("Please enter valid number : ")

operation = Bank()
operation.all_bank()
