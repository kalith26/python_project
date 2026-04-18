import itertools
import string
import time
def kali(target_password, max_length=5):
    # Defining the full character set: a-z, A-Z, 0-9, and !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    chars = string.ascii_letters + string.digits + string.punctuation
    attempts = 0
    start_time = time.time()

    print(f"[*] Character set size: {len(chars)} characters")
    
    for length in range(1, max_length + 1):
        for guess in itertools.product(chars, repeat=length):
            attempts += 1
            guess_str = ''.join(guess)

            if guess_str == target_password:
                duration = time.time() - start_time
                return f"FOUND: '{guess_str}' \nAttempts: {attempts:,}\nTime: {round(duration, 4)}s"
            
            # Progress update every 1 million attempts
            if attempts % 1000000 == 0:
                print(f"  > {attempts:,} attempts...")

    return "Password not found within length limit."
target = input("Enter a password: ")
# Example with punctuation
print(kali(target, max_length=5))
