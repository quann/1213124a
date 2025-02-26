import sys
import cv2 as cv
import numpy as np

# Các biến toàn cục
DELAY_CAPTION = 1500 #thời gian chờ giữa các bước xử lý khi hiển thị chú thích (caption). 1,5s
DELAY_BLUR = 100 #thời gian chờ giữa các bước xử lý khi hiển thị ảnh đã xử lý 0,1s
MAX_KERNEL_LENGTH = 31 # quy định kích thước tối đa của kernel (bộ lọc) trong các phương pháp làm mờ

src = None  # lưu trữ ảnh gốc
dst = None  # lưu trữ ảnh sau khi xử lý
window_name = 'Smoothing Demo'

def main(argv):
    cv.namedWindow(window_name, cv.WINDOW_AUTOSIZE)

    # Load hình ảnh
    imageName = argv[0] if len(argv) > 0 else 'vdnq.jpg'

    global src
    src = cv.imread(cv.samples.findFile(imageName))
    if src is None:
        print('lỗi khi mở ảnh')
        return -1

    if display_caption('Original Image') != 0:
        return 0

    global dst
    dst = np.copy(src)
    if display_dst(DELAY_CAPTION) != 0:
        return 0


    # Applying Gaussian blur (hiệu ứng làm mờ)
    if display_caption('Gaussian Blur') != 0:
        return 0

    ## [gaussianblur]
    for i in range(1, MAX_KERNEL_LENGTH, 2):
        dst = cv.GaussianBlur(src, (i, i), 0)   # kích thước của kernel làm mờ thay đổi từ 1x1
        display_and_save_image(dst, 'gaussian_blur_' + str(i) + '.jpg', 'Gaussian Blur')
        if display_dst(DELAY_BLUR) != 0:
            return 0
    ## [gaussianblur]
    #  Done
    display_caption('Done!')

    return 0


def display_caption(caption):
    global dst
    dst = np.zeros(src.shape, src.dtype)
    rows, cols, _ch = src.shape
    cv.putText(dst, caption,
               (int(cols / 4), int(rows / 2)),
               cv.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255))

    return display_dst(DELAY_CAPTION)


def display_dst(delay):
    cv.imshow(window_name, dst)
    c = cv.waitKey(delay)
    if c >= 0: return -1
    return 0


def display_and_save_image(image, filename, caption):
    display_image(image)
    save_image(image, filename)
    print(caption + ' saved as ' + filename)


def display_image(image):
    cv.imshow(window_name, image)
    cv.waitKey(0)


def save_image(image, filename):
    cv.imwrite(filename, image)


if __name__ == "__main__":
    main(sys.argv[1:])
