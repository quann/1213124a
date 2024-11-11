import random
import hashlib


def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Hàm tạo cặp khóa
def generate_key_pair(p):
    # Chọn một số nguyên gốc nguyên tố p
    g = 2

    # Chọn một khóa bí mật ngẫu nhiên
    x = random.randint(2, p - 2)

    # Tính khóa công khai tương ứng
    y = pow(g, x, p)

    return (p, g, y), x

# Mã hoá thông điệp từ file input.txt và ghi vào output.txt
def encrypt_file(input_filename, output_filename, public_key):
    with open(input_filename, 'r', encoding='utf-8') as input_file:
        message = input_file.read()

    encrypted_message = encrypt(message, public_key)

    # Chuyển đổi encrypted_message thành chuỗi bytes
    encrypted_message_bytes = str(encrypted_message).encode()

    with open(output_filename, 'wb') as output_file:
        output_file.write(encrypted_message_bytes)

# Giải mã thông điệp từ file input.txt và ghi vào output.txt
# Giải mã và ghi vào decrypted.txt
def decrypt_file(input_filename, output_filename, private_key):
    with open(input_filename, 'rb') as input_file:
        encrypted_message_bytes = input_file.read()

    # Chuyển đổi chuỗi bytes thành tuple
    encrypted_message = eval(encrypted_message_bytes.decode())

    # Không cần giải nén private_key ở đây
    decrypted_message = decrypt(encrypted_message, private_key)

    with open(output_filename, 'w') as output_file:
        output_file.write(decrypted_message)
# Hàm mã hoá thông điệp bằng khóa công khai

def encrypt(message, public_key):
    p, g, y = public_key
    p_minus_1 = p - 1

    # Chọn một giá trị ngẫu nhiên k sao cho 1 < k < p - 1
    k = random.randint(2, p_minus_1)

    # Tính r = g^k mod p
    r = pow(g, k, p)

    # Tính giá trị băm của thông điệp
    hash_value = hashlib.sha256(message.encode()).digest()

    # Chuyển đổi giá trị băm thành số nguyên
    hash_int = int.from_bytes(hash_value, byteorder='big')

    # Tính s = (hash - x*r) * k^(-1) mod (p - 1)
    x = public_key[1]  # Sửa lỗi ở đây, cần sử dụng public_key
    s = ((hash_int - x * r) * pow(k, p_minus_1, p)) % p_minus_1

    # Mã hoá thông điệp và trả về dưới dạng tuple (r, s)
    return (r, s)

# Hàm giải mã thông điệp bằng khóa bí mật
def decrypt(encrypted_message, private_key):
    p = private_key  # private_key chỉ là một số nguyên duy nhất trong trường hợp này

    # Tính w = s^(-1) mod (p - 1)
    w = pow(encrypted_message[1], p - 2, p - 1)

    # Tính u1 = (hash * w) mod (p - 1)
    u1 = (encrypted_message[0] * w) % (p - 1)

    # Tính u2 = (r * w) mod (p - 1)
    u2 = (encrypted_message[1] * w) % (p - 1)

    # Tính giá trị băm của thông điệp
    hash_int = (u1 * u2) % (p - 1)

    # Chuyển đổi giá trị băm thành chuỗi bytes và giải mã thông điệp
    hash_bytes = hash_int.to_bytes((hash_int.bit_length() + 7) // 8, byteorder='big')
    decrypted_message = hashlib.sha256(hash_bytes).hexdigest()

    return decrypted_message

# ...

# Sử dụng cặp khóa ElGamal để mã hoá và giải mã
p = int(input("Nhập vào một số nguyên tố: "))
if is_prime(p):
    key_pair, private_key = generate_key_pair(p)

    # Mã hoá và ghi vào output.txt
    encrypt_file("input.txt", "output.txt", key_pair)

    # Giải mã và ghi vào decrypted.txt
    decrypt_file("output.txt", "decrypted.txt", private_key)

    print("Mã hoá và giải mã thành công.")
else:
    print(f"{p} không phải là một số nguyên tố.")