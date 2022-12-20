from PIL import Image as ImagePL
import imageio
import numpy as np
import io
import base64


def convert_array_to_image(raw_data, width, height):
    data = np.zeros((height, width, 3), dtype=np.uint8)
    for row in range(height):
        for column in range(width):
            pixel = raw_data[row * width + column]
            r = pixel & 0xff
            g = (pixel >> 8) & 0xff
            b = (pixel >> 16) & 0xff
            data[row, column] = [r, g, b]

    return data


def convert_image_to_array(image):
    array_data = []
    image_dim = image.shape
    for x in range(image_dim[0]):
        for y in range(image_dim[1]):
            pixel = image[x, y]
            value = int(pixel[0] | (pixel[1] << 8) | (pixel[2] << 16))
            array_data.append(value)

    return array_data


def export_image(raw_data, file_name: str, width: int, height: int):
    image_data = convert_array_to_image(raw_data, width, height)
    image = ImagePL.fromarray(np.array(image_data), 'RGB')
    image.save(file_name)


def spread_pixel_array(data):
    new_array = []
    for pixel in data:
        new_array.append(pixel & 0xff)
        new_array.append((pixel >> 8) & 0xff)
        new_array.append((pixel >> 16) & 0xff)

    return new_array


def group_pixel_array(data):
    new_array = []
    for i in range(2, len(data), 3):
        value = data[i - 2] | (data[i - 1] << 8) | (data[i] << 16)
        new_array.append(value)

    return new_array


def import_image(file_name):
    image = imageio.imread(file_name)
    array_data = convert_image_to_array(image)
    return array_data


def export_binary(raw_data, file_name):
    image_payload = spread_pixel_array(raw_data)
    byte_array = bytes(image_payload)
    with open(file_name, 'wb') as f:
        f.write(byte_array)


def import_binary(file_name):
    with open(file_name, 'rb') as f:
        payload = b''
        for byte in iter(lambda: f.readline(), b''):
            payload += byte

        return group_pixel_array(list(payload))


def get_image(image_path):
    img = ImagePL.open(image_path, mode='r')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    encoded_img = base64.encodebytes(img_byte_arr.getvalue()).decode('ascii')
    return encoded_img


def save_image(image_data, file_name):
    with open(file_name, 'wb') as f:
        f.write(base64.decodebytes(image_data.encode()))
