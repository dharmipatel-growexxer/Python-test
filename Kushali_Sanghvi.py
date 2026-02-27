"""Bank Management System with all functionality"""
import time
from datetime import datetime
import csv
import uuid

class InvalidAmountException(Exception):
    pass
class InsufficientBalanceException(Exception):
    pass

class Bank:
    def __init__(self):
        self.current_user=None
        self.balance=0
        self.password=""
        self.name=""
        self.address=""
        self.mobile_number=""
        self.customer_key=""
        self.login_time=None
        self.number=0

    def generate_key(self):
        """Random Key Generator"""
        a=str(uuid.uuid4())[25:]
        return a

    def create_account(self):
        """Create Account with all validation check"""
        name=input("Enter your name:")
        number=int(input("Enter your mobile number:"))
        if len(str(number)) != 10:
            print("Invalid Number")
        address=input("Enter your address:")
        password=input("Enter your password:")
        if password == "" or password is None:
            print("Password is required")
        initial_deposit=int(input("Enter your initial deposit:"))
        if initial_deposit <= 0:
            print("Deposit must be positive")
        self.balance=initial_deposit
        customer_key=self.generate_key()

        # File Creation
        with open("credentials.csv", "a+") as f:
            f.write(f"{customer_key},{password}\n")
        with open("users.csv", "a+") as f:
            f.write(f"{customer_key},{name},{number},{address},{password},{initial_deposit}\n")
        with open(f"{customer_key}_transaction.csv", "a+") as f:
            f.write(f"{customer_key},{name},{initial_deposit}\n")

        print("Account created successfully")
        print(f"Your Customer Key is : {customer_key}")

    def current_date(self):
        """Current Date """
        return datetime.now().strftime("%Y-%m-%d")

    def current_time(self):
        """ Current Time"""
        return datetime.now().strftime("%H:%M:%S")

    def is_session_expired(self):
        """Check if Session is Expired or Not"""
        return (time.time() - self.login_time) > 300

    def check_session(self):
        """If Session Expired it automatically Logout"""
        if self.is_session_expired():
            self.logout()
            raise Exception("Session expired! Auto logout.")

    def login(self):
        """Login with Unique Customer Key and Password"""
        attempt=0
        while attempt<3:
             customer_key=input("Enter your customer key:")
             password=input("Enter your password:")
             with open("credentials.csv", "r") as f:
                csvreader = csv.reader(f)
                for row in csvreader:
                    if(row[0]==customer_key and row[1]==password):
                        print("Login Successful")
                        self.current_user=customer_key
                        self.login_time = time.time()

                        return

             attempt+=1
        raise Exception("3 Attempts done! Your Account is Blocked")

    def update_balance(self, amount, type):
        balance = self.get_balance() + amount

        with open(f"{self.current_user}_transaction.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([self.current_date(), self.current_time(), type, abs(amount), balance])

        # Update users.csv balance
        rows = []
        with open("users.csv", "r") as f:
            reader = csv.reader(f)
            rows = list(reader)

        for row in rows:
            if row[0] == self.current_user:
                row[4] = balance

        with open("users.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        print("Transaction Successful!")

    def deposit(self,amount):
        """Deposit Amount and update in Transaction File"""
        self.check_session()
        amount = float(amount)

        if amount <= 0:
            raise Exception("Deposit must be positive.")

        self.update_balance(amount, "DEPOSIT")


    def withdraw(self,amount):
        """Withdraw Amount and update in Transaction File"""
        self.check_session()
        amount = float(amount)

        if amount <= 0:
            raise InvalidAmountException("Invalid withdrawal amount.")

        balance = self.get_balance()
        if amount > balance:
            raise InsufficientBalanceException("Insufficient balance!")

        self.update_balance(-amount, "WITHDRAW")

    def get_balance(self):
        self.check_session()
        with open(f"{self.current_user}_transaction.csv", "r") as f:
            reader = list(csv.reader(f))
            return float(reader[-1][4])

    def check_balance(self):
        """Check Balance"""
        self.check_session()
        print("Current Balance:",self.get_balance())

    def show_details(self):
        """Show Details of User"""
        self.check_session()
        with open("users.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if row[0] == self.current_user:
                    print("\nCustomer Key:", row[0])
                    print("Name:", row[1])
                    print("Mobile:", row[2])
                    print("Address:", row[3])
                    print("Balance:", row[4])

    def update_number(self,new_mobile):
        """Update Number"""
        self.check_session()

        if len(new_mobile) != 10 or not new_mobile.isdigit():
            raise ValueError("Invalid mobile number!")

        rows = []
        with open("users.csv", "r") as f:
            rows = list(csv.reader(f))

        for row in rows:
            if row[0] == self.current_user:
                row[2] = new_mobile

        with open("users.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        print("Mobile Updated Successfully!")

    def update_address(self,new_address):
        """Update Address"""
        self.check_session()

        if not new_address:
            raise ValueError("Address cannot be empty!")

        rows = []
        with open("users.csv", "r") as f:
            rows = list(csv.reader(f))

        for row in rows:
            if row[0] == self.current_user:
                row[3] = new_address

        with open("users.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        print("Address Updated Successfully!")

    def display_passbook(self):
        self.check_session()
        print("\nDate | Time | Type | Amount | Balance\n")
        with open(f"{self.current_user}_transaction.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                print(" | ".join(row))

    def logout(self):
        """Logout from Session"""
        self.current_user=None
        print("Logout Successfully")


bank=Bank()
while True:
    print("=============Bank Management System============")
    print("1. Create Account")
    print("2. Login")
    print("3. Exit")

    c=int(input("Enter your choice:"))
    match c:
        case 1:
            bank.create_account()
        case 2:
            bank.login()
            while True:
                print("========Enter Your Choice=========")
                print("1. Deposit")
                print("2. Withdraw")
                print("3. Check Balance")
                print("4. Show user details")
                print("5. Update Mobile Number")
                print("6. Update Address")
                print("7. Display Passbook")
                print("8. Logout")

                choice = int(input("Enter your choice:"))
                match choice:
                    case 1:
                        bank.deposit(input("Amount: "))
                    case 2:
                        bank.withdraw(input("Amount: "))
                    case 3:
                        bank.check_balance()
                    case 4:
                        bank.show_details()
                    case 5:
                        bank.update_number(input("New Mobile: "))
                    case 6:
                        bank.update_address(input("New Address: "))
                    case 7:
                        bank.display_passbook()
                    case 8:
                        bank.logout()
                        break
                    case _:
                        print("Invalid Choice")
        case 3:
            break
        case _:
            print("Invalid Choice")


