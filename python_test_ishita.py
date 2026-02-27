'''Python test question
 
 
Design and implement a Bank Management System using Python.
The system must follow:
Modular programming principles
Proper file handling
Custom exception handling
Clean and maintainable code structure
The application should simulate core banking operations as described below.
🔟 Functional Requirements (10 Requirements)
1. Account Creation
Collect: Full Name, Mobile Number, Address, Password, Initial Deposit
Generate a unique Customer Key (must never change)
Validate:
Mobile number must be exactly 10 digits
Initial deposit must be positive
Password must not be empty
Store data in:
users.csv
credentials.csv
Create <customer_key>_transactions.csv
2. Login System
Login using Customer Key and Password
Validate credentials from credentials.csv
Allow maximum 3 attempts
Raise appropriate exception for invalid login
Record login time and start session timer
3. Logout System
Allow manual logout
Auto logout if session exceeds 5 minutes (300 seconds)
Display appropriate message on logout
4. Deposit Money
Accept deposit amount
Validate:
Must be numeric
Must be positive and non-zero
Raise custom exception for invalid input
Update balance
Record transaction with:
Date
Time
Type (DEPOSIT)
Amount
Updated Balance
5. Withdraw Money
Accept withdrawal amount
Validate:
Must be numeric
Must be positive
Must not exceed available balance
Raise:
InvalidAmountException
InsufficientBalanceException
Update balance and transaction file
6. Check Balance
Display current account balance
Accessible only when logged in
Must reflect latest transactions
7. Show User Details
Display:
Customer Key
Full Name
Mobile Number
Address
Current Balance
8. Update Mobile Number
Must be exactly 10 digits
Must contain only numbers
Raise exception if invalid
Update in users.csv
9. Update Address
Must not be empty
Update in users.csv
10. Display Passbook
Read user's transaction file
Display formatted output:
Date | Time | Type | Amount | Balance
Show all transactions in chronological order'''


# Bank Management System Implementation
import time
from datetime import datetime


# Custom Exceptions class
class InvalidInputException(Exception):
    pass


# Main bank management system implementation class
class BankManagementSystem:

    def __init__(self):
        self.users_file = 'users.csv'
        self.credentials_file = 'credentials.csv'
        self.users = {}
        self.credentials = {}
        self.logged_user = None
        self.session_start_time = None

    def save_users(self):
        '''This function saves users details in users.csv file'''
        with open(self.users_file, 'a') as file:
            for key, user in self.users.items():
                file.write(f"{key},{user['full_name']},{user['mobile_number']},{user['address']},{user['balance']}\n")

    def save_credentials(self):  
        '''This function saves user's credentials in credentials.csv file'''                               
        with open(self.credentials_file, 'a') as file:
            for key, password in self.credentials.items():
                file.write(f"{key},{password}\n")    

    def generate_customer_key(self, full_name, mobile_number, address):
        '''This function generates customer key'''
        return f"{full_name[:3].upper()}{mobile_number[:3]}{len(address)+len(full_name)}"
    
    def create_account(self):
        '''This function creates account for a user by taking user's data from user, checks the input validations, sends those details to saving details and credentials functions'''
        full_name = input("Enter Full Name: ")
        mobile_number = input("Enter Mobile Number: ")
        address = input("Enter Address: ")
        password = input("Enter Password: ")
        initial_deposit = input("Enter Initial Deposit: ")
        if not mobile_number.isdigit() or len(mobile_number) != 10:
            raise InvalidInputException("Mobile number must be exactly 10 digits.")
        if not password:
            raise InvalidInputException("Password cannot be empty.")
        if not initial_deposit.isdigit() or int(initial_deposit) <= 0:
            raise InvalidInputException("Initial deposit must be a positive number.")
        customer_key = self.generate_customer_key(full_name, mobile_number, address)
        self.users[customer_key] = {
            'full_name': full_name,
            'mobile_number': mobile_number,
            'address': address,
            'balance': int(initial_deposit)
        }
        self.save_users()
        self.credentials[customer_key] = password
        self.save_credentials()
        print("Account created!")
        print("Your customer key is: ", customer_key)

    def login(self):
        '''This is login function which checks if user is only attempting 3 times for login'''
        customer_key = input("Enter Customer key: ")
        password = input("Enter Password: ")
        attempts = 0
        while attempts < 3:
            if customer_key in self.credentials and self.credentials[customer_key] == password:
                self.logged_user = customer_key
                self.start_time = time.time()
                print("Login successful!")
                return
            else:
                attempts += 1
                print(f"Invalid credentials.")
        raise Exception("Maximum login attempts exceeded.")
    
    def logout(self):
        '''This is a logout function'''
        self.logged_user = None
        self.start_time = None
        print("Logged out successfully.")

    def check_session(self):
        '''This function checks how much time user has spent in that particular session and if user is exceeding 300 seconds then it will automatically log out'''
        if self.logged_user and (time.time() - self.start_time) > 300:
            print("Session expired. Logging out.")
            self.logout()

    def deposit_money(self):
        '''This function is for depositing money and then save transaction and amount in particular files'''
        self.check_session()
        amount = input("Enter deposit amount: ")
        if not amount.isdigit() or int(amount) <= 0:
            raise InvalidInputException("Deposit amount must be a positive number.")
        amount = int(amount)
        self.users[self.logged_user]['balance'] += amount
        self.save_users()
        self.record_transaction('DEPOSIT', amount)
        print(f"Deposited {amount} successfully. Current balance: {self.users[self.logged_user]['balance']}")

    def withdraw_money(self):
        '''This function is for withdrawing money and then save transaction and amount in particular files'''
        self.check_session()
        amount = input("Enter withdrawal amount: ")
        if not amount.isdigit() or int(amount) <= 0:
            raise InvalidInputException("Withdrawal amount must be a positive number.")
        amount = int(amount)
        if amount > self.users[self.logged_user]['balance']:
            raise Exception("Insufficient balance for this withdrawal.")
        self.users[self.logged_user]['balance'] -= amount
        self.save_users()
        self.record_transaction('WITHDRAW', amount)
        print(f"Withdrew {amount} successfully. Current balance: {self.users[self.logged_user]['balance']}")

    def check_balance(self):
        '''This function is for showing user their balance'''
        self.check_session()
        print(f"Current balance: {self.users[self.logged_user]['balance']}")

    def show_user_details(self):
        '''This function is for showing users their details'''
        self.check_session()
        user = self.users[self.logged_user]
        print(f"Customer Key: {self.logged_user}")
        print(f"Full Name: {user['full_name']}")
        print(f"Mobile Number: {user['mobile_number']}")
        print(f"Address: {user['address']}")
        print(f"Current Balance: {user['balance']}")

    def update_mobile_number(self):
        '''This function updates user's mobile number and checks for validations '''
        self.check_session()
        new_mobile_number = input("Enter new mobile number: ")
        if not new_mobile_number.isdigit() or len(new_mobile_number) != 10:
            raise InvalidInputException("Mobile number must be exactly 10 digits.")
        self.users[self.logged_user]['mobile_number'] = new_mobile_number
        self.save_users()
        print("Mobile number updated successfully.")

    def update_address(self):
        '''This function updates address of user after checking validation'''
        self.check_session()
        new_address = input("Enter new address: ")
        if not new_address:
            raise InvalidInputException("Address cannot be empty.")
        self.users[self.logged_user]['address'] = new_address
        self.save_users()
        print("Address updated successfully.")

    def display_passbook(self):
        '''This function display's user's passbook'''
        self.check_session()
        transactions_file = f"{self.logged_user}_transactions.csv"
        print(f"{'Date'} \t {'Time'} \t {'Type'} \t {'Amount'} \t {'Balance'} ")
        with open(transactions_file, 'r') as file:
            content = file.read()
            for i in content.splitlines():
                for j in i.split(" "):
                    print(j, end = "\t")
                print("\n")
                
        
    def record_transaction(self, transaction_type, amount):
        '''This functions records transactions of user in customerkey_transactions.csv file'''
        transactions_file = f"{self.logged_user}_transactions.csv"
        data = [datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S"), transaction_type, amount, self.users[self.logged_user]['balance']]
        with open(transactions_file, 'a') as file:
            for value in data:
                file.write(str(value))
                file.write(" ") 
            file.write("\n") 


def main():     
    '''This is the function giving user options which s/he wants to select'''
    bank = BankManagementSystem()
    while True:
        print("\n1. Create Account")
        print("2. Login")
        print("3. Logout")
        print("4. Deposit Money")
        print("5. Withdraw Money")
        print("6. Check Balance")
        print("7. Show User Details")
        print("8. Update Mobile Number")
        print("9. Update Address")
        print("10. Display Passbook")
        print("11. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            bank.create_account()
        elif choice == '2':
            bank.login()
        elif choice == '3':
            bank.logout()
        elif choice == '4':
            bank.deposit_money()
        elif choice == '5':
            bank.withdraw_money()
        elif choice == '6':
            bank.check_balance()
        elif choice == '7':
            bank.show_user_details()
        elif choice == '8':
            bank.update_mobile_number()
        elif choice == '9':
            bank.update_address()
        elif choice == '10':
            bank.display_passbook()
        elif choice == '11':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":    
    main()