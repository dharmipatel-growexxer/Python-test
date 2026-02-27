import time
import file_handling as fh
 
class InvalidAmountException(Exception):
    pass
 
class InsufficientBalanceException(Exception):
    pass
 
class InvalidMobileException(Exception):
    pass
 
class AuthenticationError(Exception):
    pass


class Bank_Management_System:
 
    def __init__(self):
        self.current_user = None
        self.login_time = None
 
 # Account Creation -----------------------------------------------------------------------------
    def create_account(self):
        name = input("Full Name: ")
        mobile = input("Mobile Number: ")
        address = input("Address: ")
        password = input("Password: ")
        try:
            deposit = float(input("Initial Deposit: "))
        except:
            raise InvalidAmountException("Deposit must be numeric")
 
        if len(mobile) != 10 or not mobile.isdigit():
            raise InvalidMobileException("Mobile must be 10 digits")
 
        if deposit <= 0:
            raise InvalidAmountException("Deposit must be positive")
 
        if password.strip() == "":
            raise Exception("Password cannot be empty")
 
        customer_key = name + str(mobile)[0:10:2]
        user_data = [customer_key, name, mobile, address, deposit]
 
        fh.write_user(user_data)
        fh.write_credentials(customer_key, password)
        fh.create_transaction_file(customer_key)
 
        fh.record_transaction(customer_key, "DEPOSIT", deposit, deposit)
 
        print("Account Created Successfully!")
        print("Customer Key:", customer_key)
 
# Login Functionality ----------------------------------------------------------------------------------------------
 
    def login(self):
        creds = fh.read_credentials()
 
        for attempt in range(3):
            key = input("Customer Key: ")
            password = input("Password: ")
 
            if key in creds and creds[key] == password:
                self.current_user = key
                self.login_time = time.time()
                print("Login Successful")
                return
            else:
                print("Invalid credentials")
 
        raise AuthenticationError("Maximum login attempts exceeded")
 
# Check Validate Session ------------------------------------------------------------------------------
 
    def check_session(self):
        if self.login_time and (time.time() - self.login_time > 300):
            print("Session expired. Auto logout.")
            self.logout()
            return False
        return True
 
# Logout Functionality --------------------------------------------------------------------------------
 
    def logout(self):
        print("Logged out successfully")
        self.current_user = None
        self.login_time = None
 
    def get_user_record(self):
        users = fh.read_users()
        for user in users:
            if user[0] == self.current_user:
                return user, users
        return None, users
 
# Deposite Functionality -------------------------------------------------------------------------
 
    def deposit(self):
        if not self.check_session():
            return
        try:
            amount = float(input("Deposit Amount: "))
        except:
            raise InvalidAmountException("Invalid amount")
 
        if amount <= 0:
            raise InvalidAmountException("Amount must be positive")
 
        user, users = self.get_user_record()
 
        balance = float(user[4]) + amount
        user[4] = str(balance)
        fh.update_users(users)
        fh.record_transaction(self.current_user, "DEPOSIT", amount, balance)
 
        print("Deposit Successful")
 
# Withdraw Functionality -----------------------------------------------------------------------
 
    def withdraw(self):
        if not self.check_session():
            return
        try:
            amount = float(input("Withdraw Amount: "))
        except:
            raise InvalidAmountException("Invalid amount")
        if amount <= 0:
            raise InvalidAmountException("Amount must be positive")
 
        user, users = self.get_user_record()
        balance = float(user[4])
 
        if amount > balance:
            raise InsufficientBalanceException("Not enough balance")
 
        balance -= amount
        user[4] = str(balance)
 
        fh.update_users(users)
        fh.record_transaction(self.current_user, "WITHDRAW", amount, balance)
 
        print("Withdraw Successful")
 
# Check Balance ------------------------------------------------------------------------------------
 
    def check_balance(self):
        if not self.check_session():
            return
        user, _ = self.get_user_record()
        print("Current Balance:", user[4])
 
# Show Details --------------------------------------------------------------------------------------------
 
    def show_details(self):
 
        if not self.check_session():
            return
 
        user, _ = self.get_user_record()
 
        print("\nCustomer Key:", user[0])
        print("Name:", user[1])
        print("Mobile:", user[2])
        print("Address:", user[3])
        print("Balance:", user[4])
 
# Update Functionality -----------------------------------------------------------------------
 
    def update_mobile(self):
 
        if not self.check_session():
            return
 
        mobile = input("New Mobile: ")
 
        if len(mobile) != 10 or not mobile.isdigit():
            raise InvalidMobileException("Invalid mobile number")
 
        user, users = self.get_user_record()
 
        user[2] = mobile
        fh.update_users(users)
 
        print("Mobile Updated Successfully")
 
# Update Functinality --------------------------------------------------------------
 
    def update_address(self):
 
        if not self.check_session():
            return
 
        address = input("New Address: ")
        if address.strip() == "":
            raise Exception("Address cannot be empty")
 
        user, users = self.get_user_record()
 
        user[3] = address
        fh.update_users(users)
 
        print("Address Updated Successfully")
 
# Passbook Functionality ------------------------------------------------------------------
 
    def show_passbook(self):
 
        if not self.check_session():
            return
 
        filename = f"{self.current_user}_transactions.csv"
 
        print("\nDate | Time | Type | Amount | Balance")
 
        with open(filename, "r") as file:
            for line in file:
                print(line.strip())

bank = Bank_Management_System()
 
while True:
 
    print("====== BANK MENU ======")
    print("1. Create Account")
    print("2. Login")
    print("3. Deposit")
    print("4. Withdraw")
    print("5. Check Balance")
    print("6. User Details")
    print("7. Update Mobile")
    print("8. Update Address")
    print("9. Passbook")
    print("10. Logout")
    print("0. Exit")
 
    choice = input("Enter choice: ")
 
    match choice:
 
            case "1":
                bank.create_account()
            case "2":
                bank.login()
            case "3":
                bank.deposit()
            case "4":
                bank.withdraw()
            case "5":
                bank.check_balance()
            case "6":
                bank.show_details()
            case "7":
                bank.update_mobile()
            case "8":
                bank.update_address()
            case "9":
                bank.show_passbook()
            case "10":
                bank.logout()
            case "0":
                break
            case _:
                print("Invalid Choice")
 