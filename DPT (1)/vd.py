import numpy as np
import matplotlib.pyplot as plt

def nhap_gia_tri_ban_dau():
    hang = int(input("Nhập số hàng của ma trận: "))
    cot = int(input("Nhập số cột của ma trận: "))
    gia_tri = np.zeros((hang, cot))

    for i in range(hang):
        for j in range(cot):
            gia_tri[i, j] = float(input(f"Nhập giá trị cho phần tử ({i+1}, {j+1}): "))

    return gia_tri

def tinh_gia_tri(x, y, sigma):
    return (1 / (2 * np.pi * sigma**2)) * np.exp(-(x**2 + y**2) / (2 * sigma**2))

def tao_ma_tran_G(gia_tri, sigma):
    hang, cot = gia_tri.shape
    ma_tran_G = np.zeros((hang, cot))

    for i in range(hang):
        for j in range(cot):
            x = j - cot // 2
            y = i - hang // 2
            ma_tran_G[i, j] = gia_tri[i, j] * tinh_gia_tri(x, y, sigma)

    return ma_tran_G

# Nhập giá trị ban đầu của ma trận
gia_tri_ban_dau = nhap_gia_tri_ban_dau()

# Tham số
sigma = 1.0

# Tạo ma trận G
ma_tran_G = tao_ma_tran_G(gia_tri_ban_dau, sigma)

# Hiển thị ma trận G
print("Ma trận G:",ma_tran_G)
