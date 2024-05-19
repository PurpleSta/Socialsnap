import hashlib

def hash_password(password):
    hasher = hashlib.md5()

    hasher.update(password.encode('utf-8'))
    hashed_password = hasher.hexdigest()
    return hashed_password

def hash_salt_password(password):
    salt = "madpamrtriwncimajun"
    salted_password = hash_password(salt + password)
    hasher = hashlib.md5()
    hasher.update(salted_password.encode('utf-8'))
    hashed_password = hasher.hexdigest()
    return hashed_password
    