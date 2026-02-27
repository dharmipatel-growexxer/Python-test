from auth import create_account,login
from transactions import deposit,withdraw,passbook,get_user , update_mobile, update_address
from helpers import Session

class Bank:
    def __init__(self):
        self.user=None
        self.session=Session()

    def register(self,*a):
        return create_account(*a)

    def login(self,key,pwd):
        login(key,pwd)
        self.user=key
        self.session.start()

    def check(self):
        self.session.validate()

    def deposit(self,a):
        self.check(); deposit(self.user,a)

    def withdraw(self,a):
        self.check(); withdraw(self.user,a)

    def details(self):
        self.check(); return get_user(self.user)

    def passbook(self):
        self.check(); return passbook(self.user)
    
    def update_mobile(self, m):
        self.check()
        update_mobile(self.user, m)

    def update_address(self, a):
        self.check()
        update_address(self.user, a)