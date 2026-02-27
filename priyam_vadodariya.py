# Functional Requirements (10 Requirements)
# 1. Account Creation
# Collect: Full Name, Mobile Number, Address, Password, Initial Deposit
# Generate a unique Customer Key (must never change)
# Validate:
# Mobile number must be exactly 10 digits
# Initial deposit must be positive
# Password must not be empty
# 
# 2.37 commit
# Store data in:
# users.csv
# credentials.csv
# Create <customer_key>_transactions.csv [also display the <customer_key>]
# 2. Login System
# Login using Customer Key and Password
# Validate credentials from credentials.csv
# Allow maximum 3 attempts
# Raise appropriate exception for invalid login
# Record login time and start session timer
# 3. Logout System
# Allow manual logout
# Auto logout if session exceeds 5 minutes (300 seconds)
# Display appropriate message on logout
# 4. Deposit Money
# Accept deposit amount
# Validate:
# Must be numeric
# Must be positive and non-zero
# Raise custom exception for invalid input
# Update balance
# Record transaction with:
# Date
# Time
# Type (DEPOSIT)
# Amount
# Updated Balance
# 5. Withdraw Money
# Accept withdrawal amount
# Validate:
# Must be numeric
# Must be positive
# Must not exceed available balance
# Raise:
# InvalidAmountException
# InsufficientBalanceException
# Update balance and transaction file
# 6. Check Balance
# Display current account balance
# Accessible only when logged in
# Must reflect latest transactions
# 7. Show User Details
# Display:
# Customer Key
# Full Name
# Mobile Number
# Address
# Current Balance
# 8. Update Mobile Number
# Must be exactly 10 digits
# Must contain only numbers
# Raise exception if invalid
# Update in users.csv
# 9. Update Address
# Must not be empty
# Update in users.csv
# 10. Display Passbook
# Read user's transaction file
# Display formatted output:
# Date | Time | Type | Amount | Balance
# Show all transactions in chronological order
from enum import Enum
import logging
import csv
import os
import uuid
from datetime import datetime, date, timedelta
# Custom exceptions

isloggedin = False
class InvalidAmountException(Exception):
    pass

class InsufficientBalanceException(Exception):
    pass

logging.basicConfig(
    filename = "bank.log",
    level = logging.INFO,
    format = "%(asctime)s - %(levelname)s - %(message)s"
)


class TransactionType(Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    CHECK_BALANCE = "balance check"



class FileHandle:
    def __init__(self, filename:str) -> None:
        self.filename = filename
    
    def read_csv(self):
        with open(self.filename, mode='r') as file:
            reader = csv.reader(file)
            data = [row for row in reader]
        return data
    
    def write_csv(self, data:list):
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)


class UserDataHandler:
    def __init__(self, users_file:str, credentials_file:str) -> None:
        self.users_file = FileHandle(users_file)
        self.credentials_file = FileHandle(credentials_file)
    
    def add_user(self, user_data:dict, credentials:dict):
        # addd user data to users_csv
        users_data = self.users_file.read_csv()
        users_data.append([user_data['customer_key'], user_data['full_name'], user_data['mobile_no'], user_data['address'], user_data["balance"]])
        self.users_file.write_csv(users_data)

        # add credentials to credentials_csv
        credentials_data = self.credentials_file.read_csv()
        credentials_data.append([credentials['customer_key'], credentials['password']])
        self.credentials_file.write_csv(credentials_data)
        transactions_filename = f"{user_data['customer_key']}_transactions.csv"

        with open(transactions_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Time", "Type", "Amount", "Balance"])

class ValidationHandler:

    @staticmethod
    def validate_mobile(mobile_no: int) -> bool:
        if len(str(mobile_no)) == 10 and str(mobile_no).isdigit():
            return True
        raise ValueError("Mobile number must be exactly 10 digits.")

    @staticmethod
    def validate_initial_deposit(amount: int) -> bool:
        if amount > 0:
            return True
        raise InvalidAmountException("Initial deposit must be positive.")

    @staticmethod
    def validate_password(password: str) -> bool:
        if password:
            return True
        raise ValueError("Password cannot be empty.")

    @staticmethod
    def validate_account_details(account_object) -> bool:
        ValidationHandler.validate_mobile(account_object.mobile_no)
        ValidationHandler.validate_initial_deposit(account_object.initial_deposit)
        ValidationHandler.validate_password(account_object.password)
        return True
# class Bank():
#     def __init__(self) -> None:
#         self.customer_id = 0

#assumption Account = customer (1:1)
class Account():
    def __init__(self, full_name:str, mobile_no:int, address : str, password: str, intial_deposit : int) -> None:
        super().__init__()
        self.full_name = full_name
        self.mobile_no = mobile_no
        self.address = address
        self.password = password
        self.initial_deposit = intial_deposit
        self.balance = intial_deposit
        self._isloggedin = False
        self.customer_key = self.generate_customer_key()

        #importing customer_id leads to everyone having same cust id
    
    #validation functions: should i create new class?
    # def validate_password(self) -> bool:
    # if self.password:
    #     return True
    # else:
    #     raise ValueError("Password must not be empty.")  

    # user details update functions
    def update_mobile(self, new_mobile_number : int):
        if ValidationHandler.validate_mobile(new_mobile_number):
            self.mobile_no = new_mobile_number
    def update_address(self, new_address : dict):
        if new_address:
            self.address = new_address
        else:
            raise ValueError("Address must not be empty.")
    def show_user_details(self):
        print(vars(self))
    
    def generate_customer_key(self):
        return str(uuid.uuid4())[:8]



# class Transaction():
#     def __int__(self):
#         pass
#     def withdraw():
#         pass

#     def deposit():
#         pass
#     def check_balance():
#         pass


# merging session and transaction into one class for now
# class Session():
#     def __int__(self):
#         pass
#     def login():
#         pass
#     def logout():
#         pass

class BankSystem():
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        users_path = os.path.join(BASE_DIR, "users.csv")
        credentials_path = os.path.join(BASE_DIR, "credentials.csv")

        # Ensure files exist
        for file in [users_path, credentials_path]:
            if not os.path.exists(file):
                open(file, 'w').close()

        self.user_data_handler = UserDataHandler(users_path, credentials_path)

        self.current_user = None
        self.session_start_time = None
    
    def get_user_data(self):
        full_name = input("Enter full name: ")
        mobile_no = int(input("Enter mobile no: "))
        address = input("Enter addresss: ")
        password = input("Enter password to be used for lgin: ")
        initial_deposit = int(input("Enter intial deposit: "))
        account_object = Account(full_name, mobile_no, address, password, initial_deposit)
        credentials = {}
        credentials['customer_key'] = account_object.customer_key
        credentials['password'] = password
        if ValidationHandler.validate_account_details(account_object):
            self.create_account(account_object, credentials)
            print("Account created successfully!")
        else:
            print("some details didn't match")
            return False


    def create_account(self, account_object:Account, credentials:dict):
        self.user_data_handler.add_user(vars(account_object), credentials)
    
    
    def login(self, customer_key:str, password:str):
       credentials_data = self.user_data_handler.credentials_file.read_csv()
       attempts = 3
       while attempts > 0:
        for record in credentials_data:
            if record[0] == customer_key and record[1] == password:
                print("Login successful.")
                logging.info(f"{customer_key} logged in")
                self.current_user = customer_key
                self.session_start_time = datetime.now()
                isloggedin = True
                return True

        attempts -= 1
        if attempts == 0:
            raise Exception("Maximum login attempts exceeded.")

        print(f"Invalid credentials. Attempts left: {attempts}")
        customer_key = input("Enter Customer Key: ")
        password = input("Enter Password: ")

        return False

    def logout(self):
        if isloggedin:
            self.session_active = False
            print("Logout successful.")
        else:
            print("No active session to logout.")
    
    def update_balance(self, new_balance):
        rows = []
        with open("users.csv", "r") as f:
            reader = csv.reader(f)
            rows = list(reader)
        for row in rows:
            if row[0] == self.current_user:
                row[4] = str(new_balance)

        with open("users.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rows)
    
    def deposit(self, amount):
        if isloggedin:
            if amount <= 0:
                raise InvalidAmountException("Deposit amount must be positive and non-zero.")
            new_balance = account_object.balance + amount
            self.update_balance(new_balance)
            self.record_transaction(TransactionType.DEPOSIT, amount, new_balance) 
    
    # def withdraw(self, customer_key:str, amount:float):
    #     if amount <= 0 or amount > self.balance:
    #         raise InvalidAmountException("Withdrawal amount must be positive and non-zero.")
        # Update balance and transaction file logic here
    def record_transaction(self, t_type, amount, balance):
        now = datetime.now()
        with open(f"{self.current_user}_transactions.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                now.strftime("%Y-%m-%d"),
                now.strftime("%H:%M:%S"),
                t_type,
                amount,
                balance

            ])

    def check_balance(self, customer_key:str):
        rows = []
        with open("users.csv", "r") as f:
            reader = csv.reader(f)
            rows = list(reader)
        for row in rows:
            if row[0] == customer_key:
                print(f"Balance for {customer_key}: {row[4]}")
                return float(row[4])
        print("Customer not found.")
        return None

    def show_user_details(self, customer_key:str):
        rows = []
        with open("users.csv", "r") as f:
            reader = csv.reader(f)
            rows = list(reader)
        for row in rows:
            if row[0] == customer_key:
                print("User Details:")
                for i, field in enumerate(["Customer Key", "Full Name", "Mobile No", "Address", "Balance"]):
                    print(f"{field}: {row[i]}")
                return
        print("Customer not found.")

if __name__ == "__main__":
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    users_path = os.path.join(BASE_DIR, "users.csv")
    credentials_path = os.path.join(BASE_DIR, "credentials.csv")

    bank = BankSystem()

    # user_data = {
    #     "full_name": "Philip Casel",
    #     "mobile_no": "9012831029",
    #     "address": "Dakota Avenue"
    # }

    # credentials = {
    #     "customer_key": "CUST001",
    #     "password": "kjash02"
    # }

    # bank.create_account(user_data, credentials)
    while(1):
        print("Welcome to Lebhagu Bank")
        print("1. Create Account")
        print("2. Login")
        print("3. Logout")
        print("4. Deposit Money")
        print("5. Withdraw Money")
        print("6. Check Balance")
        print("7. Show User Details")
        print("8. Exit")
        choice = int(input("Enter your choice"))
        match(choice):
            case 1:
                bank.get_user_data()
            case 2:
                provided_customer_id = input("Enter customer_id: ")
                provided_password = input("Enter password: ")
                bank.login(provided_customer_id, provided_password)
            case 3:
                bank.logout()
            case 4:
                deposit_amount = int(input("Amount to deposit"))
                bank.deposit(deposit_amount)
            case 8:
                exit()
            case _:
                print("Invalid choice.")
