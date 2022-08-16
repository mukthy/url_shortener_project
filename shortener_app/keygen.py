import secrets
import string


def create_random_key(length: int = 5):
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for i in range(length))
