from passlib.context import CryptContext


# Password hashing configuration
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# ─────────────────────────────
# PASSWORD HASH
# ─────────────────────────────
def hash(password: str) -> str:
    return pwd_context.hash(password)


# ─────────────────────────────
# PASSWORD VERIFY
# ─────────────────────────────
def verify(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )