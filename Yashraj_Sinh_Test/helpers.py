import csv, os, time

#Exceptions
class InvalidAmountException(Exception): pass
class InsufficientBalanceException(Exception): pass
class InvalidLoginException(Exception): pass
class SessionExpiredException(Exception): pass
class ValidationException(Exception): pass


#File handling tasks
def ensure_file(path, headers):
    if not os.path.exists(path):
        with open(path,"w",newline="") as f:
            csv.writer(f).writerow(headers)

def append_row(path,row):
    with open(path,"a",newline="") as f:
        csv.writer(f).writerow(row)

def read_all(path):
    if not os.path.exists(path): return []
    with open(path) as f:
        return list(csv.DictReader(f))

def write_all(path,fields,rows):
    with open(path,"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields)
        w.writeheader(); w.writerows(rows)


# Every Validation
def validate_mobile(m):
    if not(m.isdigit() and len(m)==10):
        raise ValidationException("Mobile must be 10 digits")

def validate_password(p):
    if not p:
        raise ValidationException("Empty Password")

def validate_amount(a):
    try:
        a=float(a)
        if a<=0: raise ValidationException("Plz enter positive Amount")
        return a
    except:
        raise ValidationException("Invalid amount")

def validate_address(addr):
    if not addr.strip():
        raise ValidationException("Address cannot be empty")


# Session Timeout -- Try 3
class Session:
    def __init__(self):
        self.login_time=None

    def start(self):
        self.login_time=time.time()

    def validate(self):
        if time.time()-self.login_time>300:
            raise SessionExpiredException("Session timeout -  exceeded 5 min ")