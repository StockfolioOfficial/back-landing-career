import re

def validate_email(email):
    result = re.match(
        r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        email
    )
    return result

def validate_password(password):
    result = re.match(
        r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[!“#$%&‘()*+,\-./:;<=>?@\[＼\]^_`{|}~\\])[A-Za-z\d!“#$%&‘()*+,\-./:;<=>?@\[＼\]^_`{|}~\\]{8,32}$',
        password
    )
    return result