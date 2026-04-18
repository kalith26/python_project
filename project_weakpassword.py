import re
import hashlib
import string

def check_password_strenght(password):
    """Check for common weak pattern and return the sha-256 hash"""
    risks =[]
    if len(password)<10:
        risks.append("Too short")
        print(len(password))

    if not re.search(r"\d", password):
        risks.append("no number")

    if not re.search(r"[A-Z]", password):
        risks.append("No upper case")
    
    if not re.search(r"[a-z]", password):
        risks.append("no lower case")

    if not any(char in string.punctuation for char in password):
        risks.append("No punctuation")

    if password.lower() in ["1234","12345678","password", "qwertyiop"]:
        risks.append("Common pattern")

    pw_hash = hashlib.sha256(password.encode()).hexdigest()
    return {"weak": len(risks)>0, "risks": risks, "hash": pw_hash}

a = input("Enter the password: ")
result = check_password_strenght(a)
print(result)
