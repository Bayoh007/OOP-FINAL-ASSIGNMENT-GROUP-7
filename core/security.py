import bcrypt

def hash_password(password: str) -> str:
    # Hash the password: encode it, generate a salt, and hash it
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Verify the password: encode both and compare
    pwd_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)




# from passlib.context import CryptContext

# pwd_context = CryptContext(
#     schemes=["bcrypt"],
#     deprecated="auto"
# )


# def hash_password(password):

#     return pwd_context.hash(password)


# def verify_password(
#         plain_password,
#         hashed_password
# ):

#     return pwd_context.verify(
#         plain_password,
#         hashed_password
#     )