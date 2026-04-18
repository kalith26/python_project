import random
import string

pass_len = 6

char = string.ascii_letters + string.digits + string.punctuation

password = ""
for i in range(pass_len):
    password += random.choice(char)

print(password)

