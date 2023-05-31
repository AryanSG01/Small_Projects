import random
import string
import bcrypt

MIN_PASSWORD_LENGTH = 8
COMPLEXITY_REQUIREMENTS = {
    "uppercase": True,
    "lowercase": True,
    "digits": True,
    "special_chars": True,
}

def generate_password():
    # Generate a random password with the specified length and complexity requirements
    characters = []
    if COMPLEXITY_REQUIREMENTS["uppercase"]:
        characters.extend(random.choices(string.ascii_uppercase, k=2))
    if COMPLEXITY_REQUIREMENTS["lowercase"]:
        characters.extend(random.choices(string.ascii_lowercase, k=2))
    if COMPLEXITY_REQUIREMENTS["digits"]:
        characters.extend(random.choices(string.digits, k=2))
    if COMPLEXITY_REQUIREMENTS["special_chars"]:
        characters.extend(random.choices(string.punctuation, k=2))

    characters.extend(random.choices(string.ascii_letters + string.digits + string.punctuation, k=MIN_PASSWORD_LENGTH - len(characters)))

    random.shuffle(characters)
    password = "".join(characters)
    return password

def encrypt_password(password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_password.decode()

def is_password_valid(password):
    # Check if the password meets the defined policies
    if len(password) < MIN_PASSWORD_LENGTH:
        return False

    if COMPLEXITY_REQUIREMENTS["uppercase"] and not any(char.isupper() for char in password):
        return False

    if COMPLEXITY_REQUIREMENTS["lowercase"] and not any(char.islower() for char in password):
        return False

    if COMPLEXITY_REQUIREMENTS["digits"] and not any(char.isdigit() for char in password):
        return False
   
    if COMPLEXITY_REQUIREMENTS["special_chars"] and not any(char in string.punctuation for char in password):
        return False

    return True

def is_password_correct(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
