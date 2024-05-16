# our modules
from passlib.context import CryptContext

# Helpers
pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


# definitions
def hash(password: str):
    return pwdContext.hash(password)


def verify(password: str, hashedPassword: str):
    return pwdContext.verify(password, hashedPassword)
