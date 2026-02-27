import csv
import os
import time
from datetime import datetime

class InvalidAmountException(Exception):
    pass


class InsufficientBalanceException(Exception):
    pass


class InvalidLoginException(Exception):
    pass


class ValidationException(Exception):
    pass


class SessionTimeoutException(Exception):
    pass

class BankManagementSystem:
    def __init__(self):
        self.current_user = None
        self.session_start_time = None
        self.init_files()

    def init_files(self):
        if not os.path.exists("users.csv"):
            with open("users.csv", 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['customer_key', 'name', 'mobile', 'address', 'balance'])
        
        if not os.path.exists("credentials.csv"):
            with open("credentials.csv", 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['customer_key', 'password'])

    # Session Management
    def check_session(self):
        if not self.current_user:
            return False
        if time.time() - self.session_start_time > 300:
            self.logout()
            raise SessionTimeoutException("Session timed out. Please login again.")
        return True

    # 1: Account Creation
    def create_account(self, name, mobile, address, password, initial_deposit):
        if len(mobile) != 10 or not mobile.isdigit():
            raise ValidationException("Mobile number must be exactly 10 digits")
        if initial_deposit <= 0:
            raise InvalidAmountException("Initial deposit must be positive")
        if not password:
            raise ValidationException("Password cannot be empty")

        customer_key = int(time.time())
        
        # Save to users.csv
        with open("users.csv", 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([customer_key, name, mobile, address, initial_deposit])

        # Save to credentials.csv
        with open("credentials.csv", 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([customer_key, password])

        # Create Transaction File
        txn_file = f"{customer_key}_transactions.csv"
        with open(txn_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Date', 'Time', 'Type', 'Amount', 'Balance'])
            now = datetime.now()
            writer.writerow([now.strftime("%d/%m/%Y"), now.strftime("%H:%M:%S"), "DEPOSIT", initial_deposit, initial_deposit])

        return customer_key
                    
    # 2: Login
    def login(self, customer_key, password):
        attempts = 0
        while attempts < 3:
            with open("credentials.csv", 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if (row['customer_key'] == customer_key and row['password'] == password):
                        self.current_user = customer_key
                        self.session_start_time = time.time()
                        return True
            attempts += 1
            print(f"Invalid credentials. Attempts left: {3 - attempts}")
            if attempts < 3:
                password = input("Enter password again: ")

        raise InvalidLoginException("Maximum login attempts exceeded.")

    # 3: Logout
    def logout(self):
        self.current_user = None
        self.session_start_time = None
        print("Logged out!!!")

    # 4 & 5: Deposit/Withdraw
    def update_balance(self, amount, txn_type):
        if amount <= 0:
            raise InvalidAmountException("Amount must be positive")

        self.check_session()
        rows = []
        updated_balance = 0
        found = False

        with open("users.csv", 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['customer_key'] == self.current_user:
                    current_bal = float(row['balance'])
                    if txn_type == "WITHDRAW":
                        if current_bal < amount:
                            raise InsufficientBalanceException("Insufficient funds.")
                        else:
                            updated_balance = current_bal - amount
                    elif txn_type == "DEPOSIT":
                        updated_balance = current_bal + amount
                    
                    row['balance'] = updated_balance
                    found = True
                rows.append(row)

        if found:
            with open("users.csv", 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            
            # Update Transaction log
            txn_file = f"{self.current_user}_transactions.csv"
            with open(txn_file, 'a', newline='') as f:
                writer = csv.writer(f)
                now = datetime.now()
                writer.writerow([now.strftime("%d/%m/%Y"), now.strftime("%H:%M:%S"), txn_type, abs(amount), updated_balance])
        return updated_balance

    # 6: Check Balance
    def get_balance(self):
        self.check_session()
        with open("users.csv", 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['customer_key'] == self.current_user:
                    return float(row['balance'])
        return None
                    
    # 7: Show User Details
    def get_user_details(self):
        self.check_session()
        with open("users.csv", 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['customer_key'] == self.current_user:
                    return row
        return None

    # 8: Update Mobile Number   
    def update_mobile(self, mobile):
        if len(mobile) != 10 or not mobile.isdigit():
            raise ValidationException("Mobile number must be exactly 10 digits.")

        self.check_session()
        rows = []
        found = False

        with open("users.csv", 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['customer_key'] == self.current_user:
                    row['mobile'] = mobile
                    found = True
                rows.append(row)

        if found:
            with open("users.csv", 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)

    # 9: Update Address
    def update_address(self, address):
        if not address or address == '':
            raise ValidationException("Address cannot be empty.")

        self.check_session()
        rows = []
        found = False

        with open("users.csv", 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['customer_key'] == self.current_user:
                    row['address'] = address
                    found = True
                rows.append(row)

        if found:
            with open("users.csv", 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)

    # 10: Display Passbook
    def show_passbook(self):
        self.check_session()
        txn_file = f"{self.current_user}_transactions.csv"
        with open(txn_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                print(f"{row[0]:<10} | {row[1]:<10} | {row[2]:<10} | {row[3]:<10} | {row[4]:<10}")


def main():
    bank = BankManagementSystem()

    while True:
        print("Enter 1 to Create Account\nEnter 2 to Login\nEnter 3 to Exit")
        option = input("Select an option: ")

        try:
            if option == '1':
                name = input("Full Name: ")
                mobile = input("Mobile: ")
                address = input("Address: ")
                password = input("Password: ")
                deposit = float(input("Initial Deposit: "))
                key = bank.create_account(name, mobile, address, password, deposit)
                print(f"Account Created! YOUR UNIQUE CUSTOMER KEY: **{key}**")

            elif option == '2':
                key = input("Customer Key: ")
                pwd = input("Password: ")
                if bank.login(key, pwd):
                    print("Login Successful!")
                    user_menu(bank)

            elif option == '3':
                break

            else: 
                print("Enter valid option!")
        except InvalidAmountException as e:
            print(f"Error: {e}")
        except ValidationException as e:
            print(f"Error: {e}")
        except InvalidLoginException as e:
            print(f"Error: {e}")

def user_menu(bank):
    while True:
        print("1. Deposit Money\n2. Withdraw Money\n3. Check Balance\n4. Show User Details\n5. Update Mobile Number\n6. Update Address\n7. Display Passbook\n8. Log Out")
        action = input("Select an action: ")
        try:
            if action == '1':
                amt = float(input("Enter amount to deposit: "))
                bank.update_balance(amt, "DEPOSIT")
                print("Deposit successful.")
            elif action == '2':
                amt = float(input("Enter amount to withdraw: "))
                bank.update_balance(amt, "WITHDRAW")
                print("Withdrawal successful.")
            elif action == '3':
                print(f"Current Balance: ${bank.get_balance()}")
            elif action == '4':
                print(bank.get_user_details())
            elif action == '5':
                new_mob = input("New Mobile: ")
                bank.update_mobile(new_mob)
            elif action == '6':
                new_addr = input("New Address: ")
                bank.update_address(new_addr)
            elif action == '7':
                bank.show_passbook()
            elif action == '8':
                bank.logout() 
                break
            else: 
                print("Enter valid option!")
        except InvalidAmountException as e:
            print(f"Cannot complete action: {e}")
        except InsufficientBalanceException as e:
            print(f"Cannot complete action: {e}")
        except InvalidLoginException as e:
            print(f"Cannot complete action: {e}")
        except ValidationException as e:
            print(f"Cannot complete action: {e}")
        except SessionTimeoutException as e:
            print(f"Cannot complete action: {e}")
        except ValueError:
            print(f"Cannot complete action: Enter valid numeric amount")


if __name__ == '__main__':
    main()