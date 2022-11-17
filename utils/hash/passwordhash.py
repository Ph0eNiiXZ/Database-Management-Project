from hashlib import sha256

def salt(password: str):
    return password + "_dQw4w9WgXcQ_" + password[::-1]

def hash(password: str):
    salted_password = salt(password)
    m = sha256()
    m.update(salted_password)
    return m.hexdigest()
