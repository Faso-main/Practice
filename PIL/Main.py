from PIL import Image
import numpy as np
import os

img_path = os.path.join('PIL', 'itr1.png')

def text_to_bits(text):
    bits = []
    for char in text:
        for byte in char.encode('utf-8'):
            bits.extend([int(b) for b in format(byte, '08b')])
    return bits

def bits_to_text(bits):
    bytes_list = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            byte += [0] * (8 - len(byte))
        bytes_list.append(int(''.join(map(str, byte)), 2))
    try:
        return bytes(bytes_list).decode('utf-8')
    except UnicodeDecodeError:
        return "Ошибка декодирования"

def encode_message_to_image(message, output_path=img_path, img_size=(100, 100)):
    bits = text_to_bits(message)
    bits_length = len(bits)
    
    width, height = img_size
    total_bits = bits_length + 32
    if width * height < total_bits:
        min_pixels = total_bits
        width = height = int(np.ceil(np.sqrt(min_pixels)))
    
    img = Image.new('L', (width, height), color=255)
    pixels = np.array(img)
    
    length_bits = [int(b) for b in format(bits_length, '032b')]
    for i in range(32):
        x, y = i % width, i // width
        if y >= height:
            break
        pixels[y, x] = 0 if length_bits[i] else 255
    
    for i in range(bits_length):
        pos = i + 32
        x, y = pos % width, pos // width
        if y >= height:
            break
        pixels[y, x] = 0 if bits[i] else 255
    
    rng = np.random.default_rng()
    noise = rng.integers(0, 50, (height, width), dtype=np.uint8)
    pixels = np.clip(pixels.astype(np.int16) - noise, 0, 255).astype(np.uint8)
    
    img = Image.fromarray(pixels)
    img.save(output_path)
    print(f"Закодировано в {output_path}")
    return img

def decode_message_from_image(image_path=img_path):
    img = Image.open(image_path)
    pixels = np.array(img).flatten()
    
    pixels = [1 if p < 128 else 0 for p in pixels]
    
    length_bits = pixels[:32]
    message_length = int(''.join(map(str, length_bits)), 2)
    
    message_bits = pixels[32:32 + message_length]
    message = bits_to_text(message_bits)
    
    return message

if __name__ == "__main__":
    encode_message_to_image(input('Введите текст: '))
    decoded_message = decode_message_from_image()
    print('Original:', decoded_message)