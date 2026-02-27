from bank_system import BankSystem
from exceptions import *

def main():
    bank = BankSystem()

    while True:
        print("\n====== BANK MANAGEMENT SYSTEM ======")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit\n")

        choice = input("Enter choice: ")

        try:
            if choice == "1":
                bank.create_account()

            elif choice == "2":
                bank.login()

                while bank.current_user:

                    print("\n1. Deposit")
                    print("2. Withdraw")
                    print("3. Balance")
                    print("4. Passbook")
                    print("5. Show User Details")
                    print("6. Update Mobile Number")
                    print("7. Update Address")
                    print("8. Logout\n")

                    opt = bank.input_with_timeout("Choose: ")

                    if opt is None:
                        break

                    if opt == "1":
                        bank.deposit()
                    elif opt == "2":
                        bank.withdraw()
                    elif opt == "3":
                        print(f"Balance: ${bank.get_balance():.2f}")
                    elif opt == "4":
                        bank.show_passbook()
                    elif opt == "5":
                        bank.show_user_details()
                    elif opt == "6":
                        bank.update_mobile()
                    elif opt == "7":
                        bank.update_address()
                    elif opt == "8":
                        bank.logout()

            elif choice == "3":
                break

        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()