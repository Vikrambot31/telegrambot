from cryptography.fernet import Fernet

# 1. Генерация ключа
key = Fernet.generate_key()
print(f"🔐 Твой секретный ключ (сохрани его в bot.py):\n{key.decode()}")

# 2. Чтение .env
with open(".env", "rb") as f:
    data = f.read()

# 3. Шифрование
f_obj = Fernet(key)
encrypted = f_obj.encrypt(data)

# 4. Сохранение в .env.enc
with open(".env.enc", "wb") as f:
    f.write(encrypted)

print("✅ .env зашифрован в .env.enc")
