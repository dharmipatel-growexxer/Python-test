import csv
import os
from datetime import datetime, timedelta


class BankingError(Exception):
    pass


class InvalidAmountException(BankingError):
    pass


class InsufficientBalanceException(BankingError):
    pass


class AuthenticationError(BankingError):
    pass


class SessionTimeoutError(BankingError):
    pass


class Bank:
    USERS_FILE = "users.csv"
    CREDENTIALS_FILE = "credentials.csv"
    COUNTER_FILE = "customer_counter.txt"

    def __init__(self):
        
        self.sessions = {}

        if not os.path.exists(self.CREDENTIALS_FILE):
            with open(self.CREDENTIALS_FILE, "w") as f:
                writer = csv.writer(f)
                writer.writerow(["customer_key", "password"])

        if not os.path.exists(self.COUNTER_FILE):
            with open(self.COUNTER_FILE, "w") as f:
                writer = csv.writer(f)
                writer.writerow(["customer_key", "password"])
                f.write("1000")
        
    def _generate_customer_key(self, full_name):
        first_name = full_name.split()[0].upper()
        with open(self.COUNTER_FILE, "r") as f:
            counter = int(f.read().strip())
        counter += 1
        with open(self.COUNTER_FILE, "w") as f:
            f.write(str(counter))
        return f"{first_name}{counter}"
    

    # helper methods for csv 
    def _append_csv(self, filename, row):
        with open(filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)

    def _read_csv(self, filename):
        if not os.path.exists(filename):
            print("filename" ,filename)
            return []
        with open(filename, "r", newline="", encoding='utf-8') as f:
            # print("filename2" ,filename)
            reader = csv.DictReader(f)
            # print(list(reader))
            data = list(reader)
            # print(data)
            return data
        

    def _write_csv(self, filename, fieldnames, rows):
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    # create account 
    def create_account(self, full_name, mobile, address, password, initial_deposit):
        if not password:
            raise ValueError("Password must not be empty")
        if not (mobile.isdigit() and len(mobile) == 10):
            raise ValueError("Mo. no. must be exactly 10 digits")
        try:
            initial_deposit = float(initial_deposit)
        except Exception:
            raise InvalidAmountException("Initial deposit must be numeric")
        if initial_deposit <= 0:
            raise InvalidAmountException("Initial deposit must be positive")

        customer_key = self._generate_customer_key(full_name)

        self._append_csv(self.USERS_FILE, [customer_key, full_name, mobile, address, f"{initial_deposit}"])
        self._append_csv(self.CREDENTIALS_FILE, [customer_key, password])

        # create transactions file
        tx_file = f"{customer_key}_transactions.csv"
        with open(tx_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "time", "type", "amount", "balance"])
            now = datetime.now()
            writer.writerow([now.date(), "INITIAL", f"{initial_deposit}", f"{initial_deposit}"])

        # tx_file = f"credentials.csv"
        # with open(tx_file, "a", newline="") as f:
        #     writer = csv.writer(f)
        #     writer.writerow(["customer_key", "password"])
        #     print(writer)

        return customer_key

  
    def login(self, customer_key, password, max_attempts=3):
        print("test")
        creds = self._read_csv(self.CREDENTIALS_FILE)
        print("creds:", creds)
        found = None
        for row in creds:
            print("row : ", row)
            if row["customer_key"] == customer_key:
                found = row
                break
        if not found:
            raise AuthenticationError("Customer key not found")

     
        attempts = 0
        while attempts < max_attempts:
            if found["password"] == password:
                self.sessions[customer_key] = {"login_time": datetime.now()}
                return True
            else:
                attempts += 1
                if attempts >= max_attempts:
                    raise AuthenticationError("Maximum login attempts exceeded")
                raise AuthenticationError("Invalid password")

    def _ensure_session(self, customer_key):
        sess = self.sessions.get(customer_key)
        if not sess:
            raise AuthenticationError("Not logged in")
        if datetime.now() - sess["login_time"] > timedelta(seconds=300):
            del self.sessions[customer_key]
            raise SessionTimeoutError("Session timed out")

    def logout(self, customer_key):
        if customer_key in self.sessions:
            del self.sessions[customer_key]

 
    def _get_user_row(self, customer_key):
        rows = self._read_csv(self.USERS_FILE)
        for r in rows:
            if r["customer_key"] == customer_key:
                return r, rows
        return None, rows

    def _update_balance_csv(self, customer_key, new_balance):
        user, rows = self._get_user_row(customer_key)
        if not user:
            raise KeyError("User not found")
        for r in rows:
            if r["customer_key"] == customer_key:
                r["balance"] = f"{new_balance}"
        self._write_csv(self.USERS_FILE, ["customer_key", "full_name", "mobile", "address", "balance"], rows)

    # deposit money
    def deposit(self, customer_key, amount):
        print("deposit called with: ", customer_key, amount)
        self._ensure_session(customer_key)
        try:
            amt = float(amount)
        except Exception:
            raise InvalidAmountException("Amount must be numeric")
        if amt <= 0:
            raise InvalidAmountException("Amount must be positive and non-zero")

        user, _ = self._get_user_row(customer_key)
        print("user in deposit: ", user)
        if not user:
            raise KeyError("User not found")

        balance = float(user["balance"])
        balance += amt
        self._update_balance_csv(customer_key, balance)
       

        # record transaction
        tx_file = f"{customer_key}_transactions.csv"
        now = datetime.now()
        self._append_csv(tx_file, [now.date(), "DEPOSIT", f"{amt}", f"{balance}"])

        return balance

    # withdraw money
    def withdraw(self, customer_key, amount):
        self._ensure_session(customer_key)
        try:
            amt = float(amount)
        except Exception:
            raise InvalidAmountException("Amount must be numeric")
        if amt <= 0:
            raise InvalidAmountException("Amount must be positive")

        user, _ = self._get_user_row(customer_key)
        if not user:
            raise KeyError("User not found")

        balance = float(user["balance"])
        if amt > balance:
            raise InsufficientBalanceException("Insufficient balance")

        balance -= amt
        self._update_balance_csv(customer_key, balance)

        tx_file = f"{customer_key}_transactions.csv"
        now = datetime.now()
        self._append_csv(tx_file, [now.date(), "WITHDRAW", f"{amt}", f"{balance}"])

        return balance

   
    def check_balance(self, customer_key):
        self._ensure_session(customer_key)
        user, _ = self._get_user_row(customer_key)
        if not user:
            raise KeyError("User not found")
        return float(user["balance"])

 
    def show_user_details(self, customer_key):
        self._ensure_session(customer_key)
        user, _ = self._get_user_row(customer_key)
        if not user:
            raise KeyError("User not found")
        return {
            "customer_key": user["customer_key"],
            "full_name": user["full_name"],
            "mobile": user["mobile"],
            "address": user["address"],
            "balance": float(user["balance"]),
        }

    def update_mobile(self, customer_key, new_mobile):
        self._ensure_session(customer_key)
        if not (new_mobile.isdigit() and len(new_mobile) == 10):
            raise ValueError("Mobile must be exactly 10 digits and numeric")
        user, rows = self._get_user_row(customer_key)
        if not user:
            raise KeyError("User not found")
        for r in rows:
            if r["customer_key"] == customer_key:
                r["mobile"] = new_mobile
        self._write_csv(self.USERS_FILE, ["customer_key", "full_name", "mobile", "address", "balance"], rows)

    def update_address(self, customer_key, new_address):
        self._ensure_session(customer_key)
        user, rows = self._get_user_row(customer_key)
        if not user:
            raise KeyError("User not found")
        for r in rows:
            if r["customer_key"] == customer_key:
                r["address"] = new_address
        self._write_csv(self.USERS_FILE, ["customer_key", "full_name", "mobile", "address", "balance"], rows)

 
    


def main():
    bank = Bank()
    logged_in_customer = None

    while True:
        print("\nBANK")
        
        if logged_in_customer:
            print(f"Logged in as: {logged_in_customer}")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Check Balance")
            print("4. Show User Details")
            print("5. Update Mobile")
            print("6. Update Address")
           
            print("7. Logout")
            print("8. Exit")
        else:
            print("1. Create Account")
            print("2. Login")
            print("3. Exit")

        choice = input("Enter choice: ")

        try:
            if not logged_in_customer:
                # Not logged in menu
                if choice == "1":
                    full_name = input("Full Name: ")
                    mobile = input("Mobile (10 digits): ")
                    address = input("Address: ")
                    password = input("Password: ")
                    initial_deposit = input("Initial Deposit: ")

                    customer_key = bank.create_account(full_name, mobile, address, password, initial_deposit)
                    print(f"Account created successfully! Customer Key: {customer_key}")

                elif choice == "2":
                    customer_key = input("Customer Key: ")
                    password = input("Password: ")

                    bank.login(customer_key, password)
                    logged_in_customer = customer_key
                    print(logged_in_customer)
                    print(f"Login successful!")

                elif choice == "3":
                    print("Thank you for using Banking System. Goodbye!")
                    break

                else:
                    print("Invalid choice")

            else:
                # Logged in menu
                if choice == "1":
                    amount = input("Enter deposit amount: ")
                    new_balance = bank.deposit(logged_in_customer, amount)
                    print(f"Deposit successful! New Balance: {new_balance}")

                elif choice == "2":
                    amount = input("Enter withdrawal amount: ")
                    new_balance = bank.withdraw(logged_in_customer, amount)
                    print(f"Withdrawal successful! New Balance: {new_balance}")

                elif choice == "3":
                    balance = bank.check_balance(logged_in_customer)
                    print(f"Current Balance: {balance}")

                elif choice == "4":
                    details = bank.show_user_details(logged_in_customer)
                    print("\n--- User Details ---")
                    for key, value in details.items():
                        print(f"{key}: {value}")

                elif choice == "5":
                    new_mobile = input("Enter new mobile number (10 digits): ")
                    bank.update_mobile(logged_in_customer, new_mobile)
                    print("Mobile number updated successfully!")

                elif choice == "6":
                    new_address = input("Enter new address: ")
                    bank.update_address(logged_in_customer, new_address)
                    print("Address updated successfully!")


                elif choice == "7":
                    bank.logout(logged_in_customer)
                    logged_in_customer = None
                    print("Logged out successfully!")

                elif choice == "8":
                    bank.logout(logged_in_customer)
                    print("Thank you for using Banking System. Goodbye!")
                    break

                else:
                    print("Invalid choice")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
