import time
from exceptions import InvalidLoginException
from bank import *


# Login and session expire check

def login():
    cred_data = read_csv('data/credentials.csv')
    attempts = 0
    while attempts < 3:
        customer_key = input("Customer Key: ").strip()
        password = input("Password: ").strip()
        for cred in cred_data:
            if cred['customer_key'] == customer_key and cred['password'] == password:
                print("\nLogin Successful!")
                start_session(customer_key)
                return
        attempts += 1
        print(f"Invalid credentials. Attempts remaining: {3 - attempts}")
    raise InvalidLoginException("Maximum login attempts exceeded.")


def start_session(customer_key):
    session_start = time.time()
    print("Session started. You will be logged out automatically after 5 minutes.")

    while True:
        elapsed = time.time() - session_start
        remaining = 300 - elapsed
        if remaining <= 0:
            print("\nSession expired! Logging out...")
            break
        print(f"\nTime remaining in session: {int(remaining)} seconds")
        print("\n=== Bank Menu ===")
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Check Balance")
        print("4. Show User Details")
        print("5. Update Mobile Number")
        print("6. Update Address")
        print("7. Display Passbook")
        print("8. Logout")
        print("")
        choice = input("Select option: ").strip()

        if choice == '1':
            deposit_money(customer_key)
        elif choice == '2':
            withdraw_money(customer_key)
        elif choice == '3':
            check_balance(customer_key)
        elif choice == '4':
            show_user_details(customer_key)
        elif choice == '5':
            update_mobile(customer_key)
        elif choice == '6':
            update_address(customer_key)
        elif choice == '7':
            display_passbook(customer_key)
        elif choice == '8':
            print("Logging out...")
            break
        else:
            print("Invalid option. Try again.")


#main menu for user input

def main():
    while True:
        print("\n=== Enter the number of your choice ===")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        print("")
        choice = input("Select option: ").strip()
        if choice == '1':
            create_account()
        elif choice == '2':
            try:
                login()
            except InvalidLoginException as e:
                print(e)
        elif choice == '3':
            print("Thank you !")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()