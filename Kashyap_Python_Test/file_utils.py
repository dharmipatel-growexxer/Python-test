import os
import csv


# present working directory
BASE_PATH = os.path.dirname(os.path.abspath(__file__))


def get_users_path():
    return os.path.join(BASE_PATH, "users.csv")

def get_credentials_path():
    return os.path.join(BASE_PATH, "credentials.csv")

# generate file when new user will create account
def get_transaction_path(customer_key):
    return os.path.join(BASE_PATH, f"{customer_key}_transactions.csv")


# check for all files
def initialize_files():
    if not os.path.exists(get_users_path()):
        with open(get_users_path(), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["CustomerKey", "Name", "Mobile", "Address", "Balance"])

    if not os.path.exists(get_credentials_path()):
        with open(get_credentials_path(), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["CustomerKey", "Password", "Locked"])