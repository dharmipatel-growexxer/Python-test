# account creation 
#login system
#logout system
#deposit money
#withdraw money
#check Balance
#show user detail
# update mobile number
#update address
#display passbook
from datetime import datetime as d
import time 
import csv 

class InvalidAmountException(Exception):
    pass

class InsufficientBalanceException(Exception):
    pass

class UserAlreadyExistsException(Exception):
    pass


def load_customer_data(customer_key):
    data = []
    with open('users.csv','r') as f:
        reader = csv.reader(f)
        for row in reader :
            if row[0]==customer_key:
                data = row
                return data
        else :
            return None

def load_customer_credentials(customer_key):
    data = []
    with open('credentials.csv','r') as f:
        reader = csv.reader(f)
        for row in reader :
            if row[0]==customer_key:
                data = row
                return data
        else :
            return None

def rewrite_user_data(customer_key,full_name,mobile_number,address,balance):
    data = [customer_key,full_name,mobile_number,address,balance]
    new_data = []
    with open("users.csv","r") as f :
        reader = csv.reader(f)
        for row in reader :
            if row[0] == customer_key:
                continue
            new_data.append(row)
    new_data.append(data)
    with open("users.csv","w") as f :
        writer = csv.writer(f)
        writer.writerows(new_data)

def rewrite_credential_data(customer_key,password,lock_status):
    data = [customer_key,lock_status,password]
    new_data = []
    with open("credentials.csv","r") as f :
        reader = csv.reader(f)
        for row in reader :
            if row[0] == customer_key:
                continue
            new_data.append(row)
    new_data.append(data)
    with open("credentials.csv","w") as f :
        writer = csv.writer(f)
        writer.writerows(new_data)

def load_customer_key():
    keys = []
    with open("users.csv",'r') as f:
        reader = csv.reader(f)
        for row in reader:
            keys.append(row[0])
    return keys 

class Bank :
    def __init__(self,balance):
        self.__balance = int(balance)
    
    def amount_validation(self,amount):
        if not amount.isdigit() or int(amount)<0 :
            raise InvalidAmountException("Amount should contain only digit and should be greater than zero")
        else :
            return True 

    def deposit(self,amount):
        if self.amount_validation(amount):
            self.__balance += int(amount)
            print(f"Successfully deposited amount {amount} in your account.")
            return self.__balance
        
    def withdraw(self,amount) :
        if self.amount_validation(amount) and int(amount)<=self.__balance:
            self.__balance -= int(amount)
            print(f"Withdraw Successfull of amount {amount}")
            return self.__balance
        else :
            raise InsufficientBalanceException("Balance is Insufficient !")

    @property
    def check_balance(self):
        return self.__balance

class user(Bank):
    def __init__(self,customer_key):
        self.user_data = load_customer_data(customer_key)
        super().__init__(self.user_data[4])

    def show_detail(self):
        customer_key = self.user_data[0]
        name = self.user_data[1]
        mobile = self.user_data[2]
        address = self.user_data[3]
        print(f"User Details :\nCustomer key : {customer_key}\nName : {name}\nmobile no. : {mobile}\naddress : {address}\nBalance : {self.check_balance}")
        

    def update_mobile(self,new_mobile):
        if new_mobile.isdigit() and int(new_mobile)>0 and len(new_mobile)==10:
            self.user_data[2] = new_mobile 
            print("Mobile number updated Successfully !")
        else :
            print("Invalid Mobile number !")

    def update_address(self,address):
        if len(address.strip()) == 0 :
            print("Address can't be empty")
        else :
            self.user_data[3] = address.strip()
            print("Address Updated Successfully !")

    def deposit(self,amount):
        self.user_data[4] = super().deposit(amount)
        with open(f"{self.user_data[0]}_transactions.csv" , "a") as f :
            time = d.now().time()
            date = d.now().date()
            type = 'Deposit'
            data = [date,time,type,amount,self.check_balance]
            writer = csv.writer(f)
            writer.writerow(data)

    def withdraw(self, amount):
        self.user_data[4] = super().withdraw(amount)
        with open(f"{self.user_data[0]}_transactions.csv" , "a") as f :
            time = d.now().time()
            date = d.now().date()
            type = 'Deposit'
            data = [date,time,type,amount,self.check_balance]
            writer = csv.writer(f)
            writer.writerow(data)
    
    def display_passbook(self):
        print("  Date   |   Time  |   Type  |   Amount    |    Balance")
        with open(f"{self.user_data[0]}_transactions.csv" , "r") as f :
            reader = csv.reader(f)
            for row in reader :
                for i in row :
                    print(i,end=' | ')
                print('\n')


def validate_amount(amount):
    if not amount.isdigit() or int(amount)<0 :
        raise InvalidAmountException("Amount should contain only digit and should be greater than zero")
    else :
        return True 

def validate_pas(pas):
    if len(pas.strip()) != len(pas) :
        print("Avoid spaces in password !")
    elif len(pas)==0 :
        print("Password can't be empty")
    else :
        return True 
        
def validate_mobile(mobile):
    if mobile.isdigit() and int(mobile)>0 and len(mobile)==10:
        return True 
    else :
        print("Enter mobile number in valid format !")



def create_account(name,mobile,add,pas,initial_deposit):
    if validate_mobile(mobile) and validate_amount(initial_deposit) and validate_pas(pas):
        customer_key = mobile[::2]+ name
        keys = load_customer_key()
        if customer_key in keys :
            raise UserAlreadyExistsException("User Already Exist !")
        else :
            with open("users.csv",'a') as f :
                writer = csv.writer(f)
                data = [customer_key,name, mobile, add,initial_deposit]
                writer.writerow(data)
            with open("credentials.csv",'a') as f :
                writer = csv.writer(f)
                data = [customer_key,pas,'0']
                writer.writerow(data)
            print(f"Account created Successfully !\nYour Customer key is : {customer_key}")



def login():
    customer_key = input("Enter customer key : ")
    data = load_customer_credentials(customer_key)
    if not data :
        print("user doesn't exists")
        time.sleep(1)
        return 
    lock_status = data[2]
    ori_password = data[1]
    if lock_status == True :
        print("Your Account is Locked !")
    if data :
        for _ in range(3):
            password = input("Enter password : ")
            if ori_password == password :
                print("Login Successful")
                new_user = user(customer_key)
                time.sleep(1)
                return new_user
            else : 
                print("Incorrect Password")
        else :
            data[2] = '1'
            print("Your Account is locked as you have exceeded maximum attempt limit !")
            rewrite_credential_data(data[0],data[1],data[2])

def main() : 
    current_user = None
    while(True):

        if current_user :
            time.sleep(1)
            print("1. Deposit Money\n2. Withdraw Money\n3. Check Balance\n4. Detials\n5. Update Mobile Number\n6. Update Address\n7. Display Passbook\n8. Logout")
            choice = input("Choose an operation to be carried out and Enter the index of operation : ")
            match choice :
                case '1' :
                    amount = input("Enter amount to deposit : ")
                    try :
                        current_user.deposit(amount)
                    except Exception as e :
                        print(e)
                case '2' :
                    amount = input("Enter amount to withdraw : ")
                    try :
                        current_user.withdraw(amount)
                    except Exception as e :
                        print(e)
                case '3' :
                    print(f"Balance : {current_user.check_balance}")
                case '4' :
                    current_user.show_detail()
                case '5' :
                    mobile = input("Enter new Mobile number : ")
                    current_user.update_mobile(mobile)
                case '6' :
                    address = input("Enter new Address : ")
                    current_user.update_address(address)
                case '7' :
                    current_user.display_passbook()
                case '8' :
                    print(f"User Logged out Successfully")
                    data = current_user.user_data
                    rewrite_user_data(data[0],data[1],data[2],data[3],data[4])
                    current_user = None 
                case _ :
                    print("You Entered an invalid choice !")

        else :
            print("1. Login\n2. Create Account\n3. Exit")
            choice = input("Choose an operation to be carried out and Enter the index of operation : ")
            match choice :
                case '1':
                        current_user = login()
                case '2':
                    print("Enter the mentioned information !")
                    name = input("Name : ")
                    mobile  = input("Mobile : ")
                    add  = input("Address : ")
                    password = input("Password : ")
                    initial_deposit  = input("Initial Deposit : ")
                    try :
                        create_account(name,mobile,add,password,initial_deposit)
                    except UserAlreadyExistsException as e:
                        print(e)
                        time.sleep(2)
                case '3' :
                    break 
                case _ :
                    print("You entered an Invalid choice !")
                    time.sleep(2)


main()