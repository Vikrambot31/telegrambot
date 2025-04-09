from cryptography.fernet import Fernet
import os

# ❗️Вставь сюда свой актуальный ключ из encrypt_env.py
key = b"tKSi68rG8Cr6bxBB662nD1gwPgkrcCi9MwVVzIVIk="  # пример — замени на свой!

fernet = Fernet(key)

with open(".env.enc", "rb") as enc_file:
    encrypted = enc_file.read()

decrypted = fernet.decrypt(encrypted)

with open(".env", "wb") as f:
    f.write(decrypted)

print("✅ Расшифровка завершена.")

