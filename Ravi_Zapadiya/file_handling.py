import csv
import os
from datetime import datetime
 
 
USERS_FILE = "users.csv"
CREDENTIALS_FILE = "credentials.csv"
 
 
def generate_customer_key():
    return "CUST" + str(int(datetime.now().timestamp()))
 
 
def create_transaction_file(customer_key):
    filename = f"{customer_key}_transactions.csv"
 
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Time", "Type", "Amount", "Balance"])
 
 
def write_user(user_data):
    with open(USERS_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(user_data)
 
def write_credentials(customer_key, password):
    with open(CREDENTIALS_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([customer_key, password])
 
def read_users():
    users = []
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            reader = csv.reader(file)
            users = list(reader)
    return users
 
def update_users(users):
    with open(USERS_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(users)
 
def read_credentials():
    creds = {}
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                creds[row[0]] = row[1]
    return creds
 
def record_transaction(customer_key, t_type, amount, balance):
    filename = f"{customer_key}_transactions.csv"
 
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
 
    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, time, t_type, amount, balance])