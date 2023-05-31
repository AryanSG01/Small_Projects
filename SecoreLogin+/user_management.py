import bcrypt
import logging
import pyotp

USER_FILE = "users.txt"
MAX_FAILED_ATTEMPTS = 3

# Configure logging
logging.basicConfig(filename="log.txt", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def is_username_available(username):
    with open(USER_FILE, "r") as file:
        for line in file:
            stored_username, _ = line.strip().split(",")
            if stored_username == username:
                return False
    return True

def lock_account(username):
    with open(USER_FILE, "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        stored_username, stored_password, failed_attempts, _, _, _ = line.strip().split(",")
        if stored_username == username:
            lines[i] = f"{stored_username},{stored_password},{int(failed_attempts) + 1}\n"
            if int(failed_attempts) + 1 >= MAX_FAILED_ATTEMPTS:
                lines[i] = f"{stored_username},{stored_password},{MAX_FAILED_ATTEMPTS}\n"  # Lock the account
                logging.warning(f"Account locked: {username}")
            break

    with open(USER_FILE, "w") as file:
        file.writelines(lines)

def deactivate_account(username):
    with open(USER_FILE, "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        stored_username, _, _, _, _, _ = line.strip().split(",")
        if stored_username == username:
            del lines[i]
            break

    with open(USER_FILE, "w") as file:
        file.writelines(lines)
        logging.info(f"Account deactivated: {username}")

def register_user(username, password, email, name):
    hashed_password = encrypt_password(password)
    secret = generate_2fa_secret()

    with open(USER_FILE, "a") as file:
        file.write(f"{username},{hashed_password},{email},{name},{secret}\n")
        logging.info(f"User registered: {username}")

def enable_2fa(username):
    with open(USER_FILE, "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        stored_username, stored_password, email, name, _ = line.strip().split(",")
        if stored_username == username:
            lines[i] = f"{stored_username},{stored_password},{email},{name},{generate_2fa_secret()}\n"
            break

    with open(USER_FILE, "w") as file:
        file.writelines(lines)
        logging.info(f"2FA enabled for user: {username}")

def verify_2fa(username, code):
    with open(USER_FILE, "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        stored_username, _, _, _, _, secret = line.strip().split(",")
        if stored_username == username:
            totp = pyotp.TOTP(secret)
            if totp.verify(code):
                logging.info(f"2FA verified for user: {username}")
                return True
            break

    return False

def encrypt_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()

def generate_2fa_secret():
    return pyotp.random_base32()

def is_password_correct(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
