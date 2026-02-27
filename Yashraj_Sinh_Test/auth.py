import uuid
from helpers import *

USERS="data/users.csv"
CREDS="data/credentials.csv"

ensure_file(USERS,["key","name","mobile","address","balance"])
ensure_file(CREDS,["key","password"])

def create_account(name,mobile,address,password,deposit):
    validate_mobile(mobile)
    validate_password(password)

    key=str(uuid.uuid4())[:8]

    append_row(USERS,[key,name,mobile,address,deposit])
    append_row(CREDS,[key,password])

    return key

def login(key,password):
    for c in read_all(CREDS):
        if c["key"]==key and c["password"]==password:
            return True
    raise InvalidLoginException("Invalid credentials")