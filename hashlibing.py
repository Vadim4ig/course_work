import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Пример хеширования пароля

print(hash_password("coacher"))