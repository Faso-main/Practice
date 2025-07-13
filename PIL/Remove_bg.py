from rembg import remove
from PIL import Image
import io
import os

img_path = os.path.join('PIL', 'img1.png')
os.makedirs(img_path, exist_ok=True)
output_path = os.path.join(img_path, 'output_image.png')

# Открываем изображение
input_path = 'cog1.jpeg'  # замените на путь к вашему изображению

with open(input_path, 'rb') as input_file:
    input_image = input_file.read()

# Удаляем фон
output_image = remove(input_image)

# Сохраняем результат
with open(output_path, 'wb') as output_file:
    output_file.write(output_image)

print("Фон успешно удален и изображение сохранено как", output_path)
