import os
import glob
from cryptography.fernet import Fernet
from multiprocessing import Pool, cpu_count


def generate_key():
    """Generate a Fernet key"""
    return Fernet.generate_key()


def test_key(args):
    """Try the `key` to decrypt the files in `directory`"""
    key, directory = args
    fernet = Fernet(key)
    for root, dirs, files in os.walk(directory):
        for file in files:
            filename = os.path.join(root, file)
            if os.path.isfile(filename) and not filename.endswith(".exe") and not filename.startswith("ransomware"):
                with open(filename, "rb") as f:
                    encrypted_data = f.read()
                try:
                    decrypted_data = fernet.decrypt(encrypted_data)
                    with open(filename, "wb") as f:
                        f.write(decrypted_data)
                    print(f"Decrypted {filename} with key {key.decode()}")
                    return key
                except:
                    continue
    return False


if __name__ == "__main__":
    directory = os.path.expanduser("~/Desktop/Test")
    success = False
    count = 0
    processes = cpu_count() * 2
    with Pool(processes=processes) as pool:
        while not success:
            # Generate a key
            key = generate_key()

            # Test the key on the encrypted files
            print(f"Testing key {key.decode()}...")
            args = [(key, directory) for _ in range(processes)]
            results = pool.map(test_key, args)
            if key in results:
                success = True
                print(f"Successful key: {key.decode()}")
            else:
                count += processes
                print(f"Tried {count:,} keys so far...")      
