import hashlib

# Chuỗi giá trị băm SHA-256
hashed_string = "084fed08b978af4d7d196a7446a86b58009e636b611db16211b65a9aadff29c5"

# Dự đoán thông điệp ban đầu và so sánh giá trị băm
message_to_hash = "dai hoc mo dia chat"  # Đây là ví dụ thông điệp ban đầu

# Băm thông điệp dự đoán
hashed_message = hashlib.sha256(message_to_hash.encode()).hexdigest()

# So sánh giá trị băm
if hashed_string == hashed_message:
    print("Thông điệp ban đầu được xác định: ", message_to_hash)
else:
    print("Không thể xác định thông điệp ban đầu.")
