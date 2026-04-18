import itertools
import string
import time

def pas(target_password, max_length=10):
    # Set of characters to try (lowercase letters + digits)
    chars = string.ascii_lowercase + string.digits
    attempts = 0
    start_time = time.time()
    print(f"[*] Starting attack on: {target_password}")

    # Iterate through possible password lengths
    for length in range(1, max_length + 1):
        # Generate all combinations for the current length
        for guess in itertools.product(chars, repeat=length):
            attempts += 1
            guess_str = ''.join(guess)

            # Check if the guess matches the target
            if guess_str == target_password:
                end_time = time.time()
                total_time = round(end_time - start_time, 4)
                return {
                    "status": "Success",
                    "password": guess_str,
                    "attempts": attempts,
                    "time": total_time
                }

    return {"status": "Failed", "attempts": attempts}

# Test the script
target = input("Enter password in 3 litters :") # Change this to test different passwords
result = pas(target)

if result["status"] == "Success":
    print(f"[+] Password found: {result['password']}")
    print(f"[+] Total attempts: {result['attempts']}")
    print(f"[+] Time taken: {result['time']} seconds")
else:
    print("[-] Password not found within the maximum length.")