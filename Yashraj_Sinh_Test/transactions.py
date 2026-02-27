import datetime
from helpers import *

USERS="data/users.csv"

def get_user(key):
    for u in read_all(USERS):
        if u["key"]==key: return u

def update_user(key,field,val):
    users=read_all(USERS)
    for u in users:
        if u["key"]==key: u[field]=val
    write_all(USERS,["key","name","mobile","address","balance"],users)

def tx_file(key):
    p=f"data/{key}_transactions.csv"
    ensure_file(p,["date","time","type","amount","balance"])
    return p

def deposit(key,amt):
    if amt<=0: raise InvalidAmountException()

    u=get_user(key)
    bal=float(u["balance"])+amt
    update_user(key,"balance",bal)

    now=datetime.datetime.now()
    append_row(tx_file(key),[now.date(),now.time(),"DEPOSIT",amt,bal])

def withdraw(key,amt):
    u=get_user(key)
    bal=float(u["balance"])

    if amt<=0: raise InvalidAmountException()
    if amt>bal: raise InsufficientBalanceException()

    bal-=amt
    update_user(key,"balance",bal)

    now=datetime.datetime.now()
    append_row(tx_file(key),[now.date(),now.time(),"WITHDRAW",amt,bal])

def passbook(key):
    return read_all(tx_file(key))

def update_mobile(key, new_mobile):
    validate_mobile(new_mobile)
    update_user(key, "mobile", new_mobile)

def update_address(key, new_addr):
    validate_address(new_addr)
    update_user(key, "address", new_addr)