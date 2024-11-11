import random
import hashlib

# Tạo cặp khóa
def generate_key_pair(p):
    # Chọn một số nguyên gốc nguyên tố p
    g = 2

    # Chọn một khóa bí mật ngẫu nhiên
    x = random.randint(2, p - 2)

    # Tính khóa công khai tương ứng
    y = pow(g, x, p)

    return (p, g, y), x

# Ký một thông điệp
def sign(message, private_key):
    p, g, y = private_key
    p_minus_1 = p - 1

    while True:
        # Chọn một giá trị ngẫu nhiên k sao cho 1 < k < p - 1
        k = random.randint(2, p_minus_1)

        # Tính r = g^k mod p
        r = pow(g, k, p)

        # Tính giá trị băm của thông điệp
        hash_value = hashlib.sha256(message.encode()).digest()

        # Chuyển đổi giá trị băm thành số nguyên
        hash_int = int.from_bytes(hash_value, byteorder='big')

        # Tính s = (hash - x*r) * k^(-1) mod (p - 1)
        x = private_key[1]
        s = ((hash_int - x * r) * pow(k, p_minus_1, p)) % p_minus_1

        if r != 0 and s != 0:
            break

    return r, s

# Xác minh chữ ký
def verify(message, signature, public_key):
    p, g, y = public_key
    r, s = signature

    if not (0 < r < p and 0 < s < p - 1):
        return False

    # Tính giá trị băm của thông điệp
    hash_value = hashlib.sha256(message.encode()).digest()

    # Chuyển đổi giá trị băm thành số nguyên
    hash_int = int.from_bytes(hash_value, byteorder='big')

    # Tính w = s^(-1) mod (p - 1)
    w = pow(s, p - 2, p - 1)

    # Tính u1 = (hash * w) mod (p - 1)
    u1 = (hash_int * w) % (p - 1)

    # Tính u2 = (r * w) mod (p - 1)
    u2 = (r * w) % (p - 1)

    # Tính v = (g^u1 * y^u2) mod p mod (p - 1)
    v = (pow(g, u1, p) * pow(y, u2, p)) % p % (p - 1)

    # Chữ ký hợp lệ nếu và chỉ nếu v == r
    return v == r

def is_prime(n):

  if n <= 1:
    return False

  for i in range(2, int(n ** 0.5) + 1):
    if n % i == 0:
      return False

  return True

p = int(input("Nhập vào một số nguyên tố : "))
if is_prime(p):
  print(f"{p} là một số nguyên tố : ")
else:
    print(f"{p} không phải là một số nguyên tố : ")
# Ví dụ sử dụng

print(p)
def write_message(message, file_path):
    with open(file_path,"w") as f:
      f.write(message)
        
message = input("Nhập thông điệp: ")
file_path = "message.txt"
key_pair, private_key = generate_key_pair(p)
signature = sign(message, key_pair)
valid = verify(message, signature, key_pair)

print("Thông điệp:", message)
print("Khóa công khai:", key_pair)
print("Khóa bí mật:", private_key)
print("Chữ ký:", signature)
print("Chữ ký hợp lệ?", valid)

write_message(message, file_path)