import csv
import time
import signal
from datetime import datetime
from exceptions import *
import file_utils

SESSION_TIMEOUT = 300


def timeout_handler(signum, frame):
    raise TimeoutException


class BankSystem:

    def __init__(self):
        self.current_user = None
        self.session_start = None
        file_utils.initialize_files()

    # unique id generator from 10000 to inf
    def generate_customer_key(self):
        users_path = file_utils.get_users_path()
        last_id = 10000

        with open(users_path, "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                try:
                    last_id = max(last_id, int(row[0]))
                except:
                    continue

        return str(last_id + 1)

    # if user will not give input in defined time session will close
    def input_with_timeout(self, prompt):
        # signal will manage the time session for the input
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(SESSION_TIMEOUT)

        try:
            # if user enters data in session time
            value = input(prompt)
            signal.alarm(0)
            self.session_start = time.time()
            return value
        # user not enter any data then automaticaly logged out
        except TimeoutException:
            signal.alarm(0)
            print("\nSession expired due to inactivity (300 seconds).")
            self.logout()
            return None

    # create account with details and some inital deposit amount
    def create_account(self):
        print('-'*50)
        name = input("Full Name: ")
        mobile = input("Mobile Number: ")
        address = input("Address: ")
        password = input("Password: ")
        deposit = input("Initial Deposit: ")

        # check for mobile number
        if not mobile.isdigit() or len(mobile) != 10:
            raise ValidationException("Mobile must be 10 digits")

        # check for password
        if not password:
            raise ValidationException("Password cannot be empty")

        # check for deposit amount
        if not deposit.replace('.', '', 1).isdigit() or float(deposit) <= 0:
            raise InvalidAmountException("Deposit must be positive")

        key = self.generate_customer_key()
        deposit_value = float(deposit)

        with open(file_utils.get_users_path(), "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([key, name, mobile, address, deposit_value])

        with open(file_utils.get_credentials_path(), "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([key, password, "False"])

        with open(file_utils.get_transaction_path(key), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Time", "Type", "Amount ($)", "Balance ($)"])

            now = datetime.now()
            writer.writerow([
                now.strftime("%Y-%m-%d"),
                now.strftime("%H:%M:%S"),
                "INITIAL_DEPOSIT",
                f"${deposit_value:.2f}",
                f"${deposit_value:.2f}"
            ])

        print("Account Created Successfully")
        print("Customer Key:", key)
        print('-'*50)

    #login and verify data from csv also set variables from none to id
    def login(self):
        attempts = 0
        print('-'*50)
        key = input("Customer Key: ")

        with open(file_utils.get_credentials_path(), "r") as f:
            rows = list(csv.reader(f))

        header = rows[0]
        data_rows = rows[1:]

        user_row = None
        for row in data_rows:
            if row[0] == key:
                user_row = row
                break

        if user_row is None:
            print("User does not exist.")
            return

        if user_row[2] == "True":
            raise AccountLockedException("Account is locked permanently.")

        while attempts < 3:
            password = input("Password: ")

            # set current user to that unique key
            if password == user_row[1]:
                self.current_user = key
                self.session_start = time.time()
                print("Login Successful")
                print('-'*50)
                return

            attempts += 1
            print("Invalid password. Attempts left:", 3 - attempts)

        for row in data_rows:
            if row[0] == key:
                row[2] = "True"

        with open(file_utils.get_credentials_path(), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data_rows)
        print('-'*50)

        raise AccountLockedException("Account locked after 3 failed attempts.")
    

    # logout the session by setting veriable none
    def logout(self):
        self.current_user = None
        self.session_start = None
        print("Logged out successfully")
        print('-'*50)

    # get user details from csv data
    def show_user_details(self):
        print('-'*50)
        with open(file_utils.get_users_path(), "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if row[0] == self.current_user:
                    print("\nCustomer Key:", row[0])
                    print("Full Name:", row[1])
                    print("Mobile:", row[2])
                    print("Address:", row[3])
                    print(f"Balance: ${float(row[4]):.2f}")
                    print('-'*50)
                    return

    # update mobile number
    def update_mobile(self):
        print('-'*50)
        new_mobile = self.input_with_timeout("Enter new mobile number: ")
        if new_mobile is None:
            return

        if not new_mobile.isdigit() or len(new_mobile) != 10:
            raise ValidationException("Mobile must be exactly 10 digits")

        rows = []
        with open(file_utils.get_users_path(), "r") as f:
            rows = list(csv.reader(f))

        for row in rows:
            if row[0] == self.current_user:
                row[2] = new_mobile

        with open(file_utils.get_users_path(), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        print("Mobile number updated successfully")
        print('-'*50)
        
    # update address town
    def update_address(self):
        print('-'*50)
        new_address = self.input_with_timeout("Enter new address: ")
        if new_address is None:
            return

        if not new_address.strip():
            raise ValidationException("Address cannot be empty")

        rows = []
        with open(file_utils.get_users_path(), "r") as f:
            rows = list(csv.reader(f))

        for row in rows:
            if row[0] == self.current_user:
                row[3] = new_address.strip()

        with open(file_utils.get_users_path(), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        print("Address updated successfully")
        print('-'*50)


    # to check balance from csv files by getting path from file_utils.py
    def get_balance(self):
        print('-'*50)
        with open(file_utils.get_users_path(), "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if row[0] == self.current_user:
                    return float(row[4])
        
                
    
    # updating the balance in csv files if it deposited or withdrawed
    def update_balance(self, new_balance):
        rows = []
        with open(file_utils.get_users_path(), "r") as f:
            rows = list(csv.reader(f))

        for row in rows:
            if row[0] == self.current_user:
                row[4] = str(new_balance)

        with open(file_utils.get_users_path(), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    # it will record transactions with day-time and amount
    def record_transaction(self, t_type, amount, balance):
        now = datetime.now()

        with open(file_utils.get_transaction_path(self.current_user), "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                now.strftime("%Y-%m-%d"),
                now.strftime("%H:%M:%S"),
                t_type,
                f"${float(amount):.2f}",
                f"${float(balance):.2f}"
            ])
    # it will update deposit amount in csv data and print final balance
    def deposit(self):
        print('-'*50)
        amount = self.input_with_timeout("Deposit amount: ")
        if amount is None:
            return

        if not amount.replace('.', '', 1).isdigit() or float(amount) <= 0:
            raise InvalidAmountException("Invalid deposit amount")

        balance = self.get_balance()
        new_balance = balance + float(amount)

        self.update_balance(new_balance)
        self.record_transaction("DEPOSIT", amount, new_balance)

        print(f"Deposit successful. New Balance: ${new_balance:.2f}")
        print('-'*50)

    # it change net balance by withdrawing amount
    def withdraw(self):
        print('-'*50)
        amount = self.input_with_timeout("Withdraw amount: ")
        if amount is None:
            return

        if not amount.replace('.', '', 1).isdigit() or float(amount) <= 0:
            raise InvalidAmountException("Invalid withdrawal amount")

        balance = self.get_balance()

        if float(amount) > balance:
            raise InsufficientBalanceException("Insufficient balance")

        new_balance = balance - float(amount)

        self.update_balance(new_balance)
        self.record_transaction("WITHDRAW", amount, new_balance)

        print(f"Withdrawal successful. New Balance: ${new_balance:.2f}")
        print('-'*50)

    # print transaction history with initial transaction
    def show_passbook(self):
        print("\nDate        Time      Type              Amount       Balance")
        print("-" * 70)

        with open(file_utils.get_transaction_path(self.current_user), "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                print("{:<12} {:<10} {:<16} {:<12} {:<12}".format(*row))
        print('-'*70)