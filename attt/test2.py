import random
import hashlib
import pickle


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
def encrypt_file(input_filename, output_filename, public_key):
    with open(input_filename, 'rb') as input_file:  # Open in binary mode
        message = input_file.read()

    encrypted_message = encrypt(message, public_key)

    with open(output_filename, 'wb') as output_file:  # Open in binary mode
        # Write the encrypted_message as binary data
        output_file.write(encrypted_message)

def decrypt_file(input_filename, output_filename, private_key):
    with open(input_filename, 'rb') as input_file:  # Open in binary mode
        encrypted_message = input_file.read()

    decrypted_message_bytes = decrypt(encrypted_message, private_key)

    with open(output_filename, 'wb') as output_file:  # Open in binary mode
        # Write the decrypted binary message directly
        output_file.write(decrypted_message_bytes)
# In the encrypt function, you can hash the binary data directly:
def encrypt(message, public_key):
    p, g, y = public_key
    p_minus_1 = p - 1

    k = random.randint(2, p_minus_1)

    r = pow(g, k, p)

    hash_value = hashlib.sha256(message).digest()

    hash_int = int.from_bytes(hash_value, byteorder='big')

    x = public_key[2]
    s = ((hash_int - x * r) * pow(k, p_minus_1, p)) % p_minus_1

    # Serialize the (r, s) tuple to bytes using pickle
    encrypted_message = pickle.dumps((r, s))

    return encrypted_message 

# In the decrypt function, you can decode the message to UTF-8 text:
def decrypt(encrypted_message, private_key):
    p = private_key

    w = pow(encrypted_message[1], p - 2, p - 1)

    u1 = (encrypted_message[0] * w) % (p - 1)
    u2 = (encrypted_message[1] * w) % (p - 1)

    hash_int = (u1 * u2) % (p - 1)

    hash_bytes = hash_int.to_bytes((hash_int.bit_length() + 7) // 8, byteorder='big')
    decrypted_message = hashlib.sha256(hash_bytes).digest()

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