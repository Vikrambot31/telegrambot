from cryptography.fernet import Fernet
import os

key = b"вставь_сюда_твой_секретный_ключ"

fernet = Fernet(key)

with open(".env.enc", "rb") as enc_file:
    encrypted = enc_file.read()

decrypted = fernet.decrypt(encrypted)

with open(".env", "wb") as f:
    f.write(decrypted)

print("✅ Расшифровка завершена.")
