# install passlib which is used to encrypt the data 


from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash(password : str):
    return pwd_context.hash(password)


def varify_pass(plain_pass, hashed_pass):
    return pwd_context.verify(plain_pass, hashed_pass)
