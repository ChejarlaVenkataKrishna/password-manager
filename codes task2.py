from cryptography.fernet import Fernet
import json
import os

class PasswordManager:
    def __init__(self, master_password):
        self.master_password = master_password
        self.key = self._load_or_create_key()
        self.data = self._load_data()

    def _load_or_create_key(self):
        key_file = "encryption_key.key"
        if os.path.exists(key_file):
            with open(key_file, "rb") as file:
                key = file.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, "wb") as file:
                file.write(key)
        return key

    def _encrypt(self, data):
        cipher = Fernet(self.key)
        encrypted_data = cipher.encrypt(data.encode())
        return encrypted_data

    def _decrypt(self, encrypted_data):
        cipher = Fernet(self.key)
        decrypted_data = cipher.decrypt(encrypted_data).decode()
        return decrypted_data

    def _load_data(self):
        data_file = "passwords.json"
        data = {}
        if os.path.exists(data_file):
            with open(data_file, "rb") as file:
                encrypted_data = file.read()
            try:
                decrypted_data = self._decrypt(encrypted_data)
                data = json.loads(decrypted_data)
            except Exception as e:
                print("Error decrypting data:", e)
        return data

    def _save_data(self):
        data_file = "passwords.json"
        encrypted_data = self._encrypt(json.dumps(self.data))
        with open(data_file, "wb") as file:
            file.write(encrypted_data)

    def add_password(self, website, username, password):
        if website not in self.data:
            self.data[website] = {"username": username, "password": password}
            self._save_data()
            print(f"Password for {website} added successfully.")
        else:
            print(f"Password for {website} already exists. Use update_password method to change it.")

    def get_password(self, website):
        if website in self.data:
            return self.data[website]["password"]
        else:
            print(f"No password found for {website}.")

    def update_password(self, website, new_password):
        if website in self.data:
            self.data[website]["password"] = new_password
            self._save_data()
            print(f"Password for {website} updated successfully.")
        else:
            print(f"No password found for {website}.")

# Example usage:
master_password = input("Enter your master password: ")
password_manager = PasswordManager(master_password)

password_manager.add_password("example.com", "user123", "securepass123")
print("Retrieved password:", password_manager.get_password("example.com"))

password_manager.update_password("example.com", "newpass456")
print("Updated password:", password_manager.get_password("example.com"))
