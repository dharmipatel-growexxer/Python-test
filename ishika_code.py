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

class BankSystem:
   def __init__(self):
       self.current_user = None
       self.session_start = None
       self.initialize_files()
  
   def initialize_files(self):
       if not os.path.exists("users.csv"):
           with open("users.csv", "w", newline="") as f:
               writer = csv.writer(f)
               writer.writerow(["CustomerKey", "Name", "Mobile", "Address", "Balance"])
       if not os.path.exists("credentials.csv"):
           with open("credentials.csv", "w", newline="") as f:
               writer = csv.writer(f)
               writer.writerow(["CustomerKey", "Password"])
   def create_account(self):
       name = input("enter Full Name: ")
       mobile = input("enter Mobile Number: ")
       address = input("enter Address: ")
       password = input("enter your Password: ")
       deposit = input("enter Initial Deposit: ")
       if not mobile.isdigit() or len(mobile) != 10:
           raise ValidationException("Mobile number should be of 10 digits")
       if not password:
           raise ValidationException("Password should not be empty")
       if not deposit.replace('.', '', 1).isdigit() or float(deposit) <= 0:
           raise InvalidAmountException("Deposit amount should be positive")
       customer_key = "CUST" + str(int(time.time()))
       with open("users.csv", "a", newline="") as f:
           writer = csv.writer(f)
           writer.writerow([customer_key, name, mobile, address, float(deposit)])
       with open("credentials.csv", "a", newline="") as f:
           writer = csv.writer(f)
           writer.writerow([customer_key, password])
       with open(f"{customer_key}_transactions.csv", "w", newline="") as f:
           writer = csv.writer(f)
           writer.writerow(["Date", "Time", "Type", "Amount", "Balance"])
       print("Your Account Created Successfully!")
       print("Your Customer Key:", customer_key)
   def login(self):
       attempts = 0
       while attempts < 3:
           key = input("Customer Key: ")
           password = input("Password: ")
           with open("credentials.csv", "r") as f:
               reader = csv.reader(f)
               next(reader)
               for row in reader:
                   if row[0] == key and row[1] == password:
                       self.current_user = key
                       self.session_start = time.time()
                       print("Login Successful!")
                       return
           attempts += 1
           print("Invalid credentials. Attempts left:", 3 - attempts)
       raise InvalidLoginException("Max login attempts exceeded.")
   def check_session(self):
       if self.session_start:
           if time.time() - self.session_start > 300:
               print("Session expired (5 minutes). Auto logout.")
               self.logout()
   def logout(self):
       self.current_user = None
       self.session_start = None
       print("Logged out successfully")
   def get_balance(self):
       with open("users.csv", "r") as f:
           reader = csv.reader(f)
           next(reader)
           for row in reader:
               if row[0] == self.current_user:
                   return float(row[4])
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
   def record_transaction(self, t_type, amount, balance):
       now = datetime.now()
       with open(f"{self.current_user}_transactions.csv", "a", newline="") as f:
           writer = csv.writer(f)
           writer.writerow([
               now.strftime("%Y-%m-%d"),
               now.strftime("%H:%M:%S"),
               t_type,
               amount,
               balance
           ])
   def deposit(self):
       amount = input("Enter deposit amount: ")
       if not amount.replace('.', '', 1).isdigit() or float(amount) <= 0:
           raise InvalidAmountException("Invalid deposit amount")
       balance = self.get_balance()
       new_balance = balance + float(amount)
       self.update_balance(new_balance)
       self.record_transaction("DEPOSIT", amount, new_balance)
       print("Amount Deposited successful")
   def withdraw(self):
       amount = input("Enter withdrawal amount: ")
       if not amount.replace('.', '', 1).isdigit() or float(amount) <= 0:
           raise InvalidAmountException("Invalid withdrawal amount")
       balance = self.get_balance()
       if float(amount) > balance:
           raise InsufficientBalanceException("Insufficient balance")
       new_balance = balance - float(amount)
       self.update_balance(new_balance)
       self.record_transaction("WITHDRAW", amount, new_balance)
       print("Amount Withdrawal successfully")
   def show_balance(self):
       print("Current Balance:", self.get_balance())
   def show_user_details(self):
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
   def update_mobile(self):
       new_mobile = input("New Mobile Number: ")
       if not new_mobile.isdigit() or len(new_mobile) != 10:
           raise ValidationException("Invalid mobile number")
       rows = []
       with open("users.csv", "r") as f:
           rows = list(csv.reader(f))
       for row in rows:
           if row[0] == self.current_user:
               row[2] = new_mobile
       with open("users.csv", "w", newline="") as f:
           writer = csv.writer(f)
           writer.writerows(rows)
       print("your Mobile number updated")
   def update_address(self):
       new_address = input("New Address is : ")
       if not new_address.strip():
           raise ValidationException("Address cannot be empty")
       rows = []
       with open("users.csv", "r") as f:
           rows = list(csv.reader(f))
       for row in rows:
           if row[0] == self.current_user:
               row[3] = new_address
       with open("users.csv", "w", newline="") as f:
           writer = csv.writer(f)
           writer.writerows(rows)
       print("Address updated!")
   def show_passbook(self):
       print("\nDate        Time      Type       Amount     Balance")
       print("-" * 55)
       with open(f"{self.current_user}_transactions.csv", "r") as f:
           reader = csv.reader(f)
           next(reader)
           for row in reader:
               print("{:<12} {:<10} {:<10} {:<10} {:<10}".format(*row))

def main():
   bank = BankSystem()
   while True:
       print(" BANK MANAGEMENT SYSTEM ")
       print("1. Create Account")
       print("2. Login")
       print("3. Exit")
       choice = input("Enter choice: ")
       try:
           if choice == "1":
               bank.create_account()
           elif choice == "2":
               bank.login()
               while bank.current_user:
                   bank.check_session()
                   print("\n--- Banking Menu ---")
                   print("1. Deposit")
                   print("2. Withdraw")
                   print("3. Check Balance")
                   print("4. Show User Details")
                   print("5. Update Mobile")
                   print("6. Update Address")
                   print("7. Passbook")
                   print("8. Logout")
                   option = input("Choose option: ")
                   if option == "1":
                       bank.deposit()
                   elif option == "2":
                       bank.withdraw()
                   elif option == "3":
                       bank.show_balance()
                   elif option == "4":
                       bank.show_user_details()
                   elif option == "5":
                       bank.update_mobile()
                   elif option == "6":
                       bank.update_address()
                   elif option == "7":
                       bank.show_passbook()
                   elif option == "8":
                       bank.logout()
           elif choice == "3":
               print("Thank you for using the system.")
               break
       except Exception as e:
           print("Error:", e)

if __name__ == "__main__":
   main()
