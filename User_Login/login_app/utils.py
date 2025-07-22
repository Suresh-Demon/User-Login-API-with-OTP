import random ,datetime ,jwt

def generate_otp():
    return str(random.randint(100000, 999999))

def generate_token(user):
    payload = {
        'email' : user.email,
        'exp'   : datetime.datetime.utcnow() +  datetime.timedelta(hours=1)
    }
    return jwt.encode (payload,"secret", algorithm='HS256')

