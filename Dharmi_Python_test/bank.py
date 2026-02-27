"""
    This file contains various functions related to banking. 
    It contains basic functions such as: 
    1. Customer key generation : It generates unique customer key everytime an user creates new account.
    2. Mobile number validation: Validates the mobile number that it should contain 10 digits. 
    3. Password validation: Validates the password 
    4. csv reading ,writing and adding

    It contains functions related to user like: 
    1. Create new account
    2. Login into existing account
    3. View account details and balance
    4. withdraw and deposit money
    5. Update address and mobile number 
"""

import csv
import os
import uuid
import time
from datetime import datetime
from exceptions import InvalidInputException, InsufficientBalanceException


def generate_customer_key():
    # return "CUST" + datetime.now().strftime("%Y%m%d%H%M%") 
    return "CUST-"+str(uuid.uuid4())+"-"+datetime.now().strftime("%Y%m%d%H%M")

def validate_mobile_number(mobile):
    if not mobile.isdigit() or len(mobile) != 10:
        raise InvalidInputException("Mobile number must be exactly 10 digits.")
    

def validate_password(password):
    if not password.strip() or len(password) > 8:
        raise InvalidInputException("Password cannot be empty.")

def validate_amount(amount):
    try:
        value = float(amount)
    except ValueError:
        raise InvalidInputException("Amount must be numeric.")
    if value <= 0:
        raise InvalidInputException("Amount must be positive and non-zero.")
    return value

def read_csv(file):
    if not os.path.exists(file):
        return []
    with open(file, mode='r', newline='') as f:
        return list(csv.DictReader(f))

def write_csv(file, data, fieldnames):
    with open(file, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def append_csv(file, row, fieldnames):
    file_exists = os.path.exists(file)
    with open(file, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


#functions related to account creation, deposit, withdraw , balance check and update details 

def create_account():
    print("\n=== Account Creation ===")
    name = input("Full Name: ").strip()

   
    while True:
        mobile = input("Mobile Number: ").strip()
        try:
            validate_mobile_number(mobile)
            break  
        except InvalidInputException as e:
            print("Error:", e)
            print("Please re-enter mobile number.")

    address = input("Address: ").strip()

    while True:
        password = input("Password: ").strip()
        try:
            validate_password(password)
            break
        except InvalidInputException as e:
            print("Error:", e)
            print("Please re-enter password.")

    while True:
        initial_deposit = input("Initial Deposit: ").strip()
        try:
            initial_deposit = validate_amount(initial_deposit)
            break
        except InvalidInputException as e:
            print("Error:", e)
            print("Please enter a valid initial deposit amount.")

    customer_key = generate_customer_key()

    user_data = read_csv('data/users.csv')
    user_data.append({
        'customer_key': customer_key,
        'name': name,
        'mobile': mobile,
        'address': address,
        'balance': f"{initial_deposit:.2f}"
    })
    write_csv('data/users.csv', user_data, ['customer_key','name','mobile','address','balance'])

    cred_data = read_csv('data/credentials.csv')
    cred_data.append({'customer_key': customer_key, 'password': password})
    write_csv('data/credentials.csv', cred_data, ['customer_key','password'])

    
    transaction_file = f"data/{customer_key}_transactions.csv"
    append_csv(transaction_file, {
        'date': datetime.now().strftime("%Y-%m-%d"),
        'time': datetime.now().strftime("%H:%M:%S"),
        'type': 'INITIAL_DEPOSIT',
        'amount': f"{initial_deposit:.2f}",
        'balance': f"{initial_deposit:.2f}"
    }, ['date','time','type','amount','balance'])

    print(f"\nAccount created successfully! Your Customer Key is: {customer_key}")



def get_user_record(customer_key):
    users = read_csv('data/users.csv')
    print("==============================")
    for user in users:
        if user['customer_key'] == customer_key:
            return user
    return None




def update_user_record(updated_record):
    users = read_csv('data/users.csv')
    for i, user in enumerate(users):
        if user['customer_key'] == updated_record['customer_key']:
            users[i] = updated_record
            break
    write_csv('data/users.csv', users, ['customer_key','name','mobile','address','balance'])


#operations like deposit, balance check , withdraw etc\

def deposit_money(customer_key):
    user = get_user_record(customer_key)
    print("==============================")
    if not user:
        print("User not found!")
        return
    amount = input("Enter deposit amount: ").strip()
    try:
        amount = validate_amount(amount)
    except InvalidInputException as e:
        print("Error:", e)
        return
    user['balance'] = f"{float(user['balance']) + amount:.2f}"
    update_user_record(user)
    transaction_file = f"data/{customer_key}_transactions.csv"
    append_csv(transaction_file, {
        'date': datetime.now().strftime("%Y-%m-%d"),
        'time': datetime.now().strftime("%H:%M:%S"),
        'type': 'DEPOSIT',
        'amount': f"{amount:.2f}",
        'balance': user['balance']
    }, ['date','time','type','amount','balance'])
    print("===============================")
    print(f"Deposited successfully! New Balance: {user['balance']}")

def withdraw_money(customer_key):
    print("==============================")
    user = get_user_record(customer_key)
    if not user:
        print("User not found!")
        return
    amount = input("Enter withdrawal amount: ").strip()
    try:
        amount = validate_amount(amount)
        if amount > float(user['balance']):
            raise InsufficientBalanceException("Insufficient balance!")
    except (InvalidInputException, InsufficientBalanceException) as e:
        print("Error:", e)
        return
    user['balance'] = f"{float(user['balance']) - amount:.2f}"
    update_user_record(user)
    transaction_file = f"data/{customer_key}_transactions.csv"
    append_csv(transaction_file, {
        'date': datetime.now().strftime("%Y-%m-%d"),
        'time': datetime.now().strftime("%H:%M:%S"),
        'type': 'WITHDRAW',
        'amount': f"{amount:.2f}",
        'balance': user['balance']
    }, ['date','time','type','amount','balance'])
    print(f"Withdrawal successful! New Balance: {user['balance']}")



def check_balance(customer_key):
    user = get_user_record(customer_key)
    print("==============================")
    if user:
        print(f"Current Balance: {user['balance']}")
    else:
        print("User not found!")



def show_user_details(customer_key):
    user = get_user_record(customer_key)
    print("==============================")
    if user:
        print("\n=== User Details ===")
        print(f"Customer Key: {user['customer_key']}")
        print(f"Full Name: {user['name']}")
        print(f"Mobile Number: {user['mobile']}")
        print(f"Address: {user['address']}")
        print(f"Current Balance: {user['balance']}")
    else:
        print("User not found!")



def update_mobile(customer_key):
    user = get_user_record(customer_key)
    print("==============================")
    if not user:
        print("User not found!")
        return
    new_mobile = input("Enter new mobile number: ").strip()
    try:
        validate_mobile_number(new_mobile)
    except InvalidInputException as e:
        print("Error:", e)
        return
    user['mobile'] = new_mobile
    update_user_record(user)
    print("Mobile number updated successfully!")



def update_address(customer_key):
    print("==============================")
    user = get_user_record(customer_key)
    if not user:
        print("User not found!")
        return
    new_address = input("Enter new address: ").strip()
    if not new_address:
        print("Address cannot be empty!")
        return
    user['address'] = new_address
    update_user_record(user)
    print("Address updated successfully!")



def display_passbook(customer_key):
    transaction_file = f"data/{customer_key}_transactions.csv"
    if not os.path.exists(transaction_file):
        print("No transactions found!")
        return
    transactions = read_csv(transaction_file)
    print("\n========== Passbook ==========")
    print(f"{'Date':<12} {'Time':<10} {'Type':<15} {'Amount':<10} {'Balance':<10}")
    for tx in transactions:
        print(f"{tx['date']:<12} {tx['time']:<10} {tx['type']:<15} {tx['amount']:<10} {tx['balance']:<10}")


