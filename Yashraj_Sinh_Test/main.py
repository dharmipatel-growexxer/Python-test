from bank import Bank
from helpers import *

bank=Bank()

while True:
    print("\n1.Create Account 2.Login 3.Exit")
    ch=input("Choice: ")
    
    if ch=="3":
        print("Exiting system...")
        break

    if ch=="1":
        name=input("Name: ")
        mob=input("Mobile: ")
        addr=input("Address: ")
        pwd=input("Password: ")
        dep=validate_amount(input("Deposit: "))
        key=bank.register(name,mob,addr,pwd,dep)
        print("Customer Key:",key)

    elif ch=="2":
        attempts=0
        while attempts<3:
            try:
                key=input("Key: ")
                pwd=input("Password: ")
                bank.login(key,pwd)
                print("Login success")
                break
            except InvalidLoginException as e:
                attempts+=1
                print(e)

        if attempts==3:
            raise InvalidLoginException("3 failed attempts")

        while True:
            try:
                print("\n1.Deposit 2.Withdraw 3.Details 4.Passbook 5.Update Mobile 6.Update Address 7.Logout")
                op=input("Choice: ")

                if op=="1": bank.deposit(validate_amount(input("Amount: ")))
                elif op=="2": bank.withdraw(validate_amount(input("Amount: ")))
                elif op=="3": print(bank.details())
                elif op=="4":
                    data = bank.passbook()
                    if not data:
                        print("No transactions yet")
                    else:
                        print("\nDate | Time | Type | Amount | Balance")
                        for r in data:
                            print(f"{r['date']} | {r['time']} | {r['type']} | {r['amount']} | {r['balance']}")
                # elif op=="4":
                #     for r in bank.passbook(): print(r)
                

                elif op=="5":
                    m=input("New Mobile: ")
                    bank.update_mobile(m)
                    print("Mobile updated")

                elif op=="6":
                    a=input("New Address: ")
                    bank.update_address(a)
                    print("Address updated")
                
                else: break
                
            except SessionExpiredException as e:
                print(e)
                break