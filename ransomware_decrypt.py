import os
from cryptography.fernet import Fernet

# Get the key from user input
key = input("Enter the encryption key: ").encode()

# Create the Fernet object
fernet = Fernet(key)

# Get the directory to decrypt
directory = input("Enter the directory to decrypt: ")

# Walk through the directory and decrypt all files
for root, dirs, files in os.walk(directory):
    for file in files:
        filename = os.path.join(root, file)
        # Check if the file is a regular file
        if os.path.isfile(filename):
            if filename.endswith(".exe"):
                continue
            if filename.startswith("ransomware"):
                continue
            with open(filename, "rb") as f:
                encrypted_data = f.read()
            try:
                decrypted_data = fernet.decrypt(encrypted_data)
                with open(filename, "wb") as f:
                    f.write(decrypted_data)
                print(f"Decrypted {filename}")
            except:
                print(f"Failed to decrypt {filename}")
        else:
            print(f"Skipping non-file {filename}")

print("Decryption complete.")
