from PIL import Image
from sys import argv, exit

def main():
    try:
        filepath = argv[1]
    except Exception:
        print("""Формат конвертирования: [Фото] [разрешение]*\nПример: photo.png 48\nДопустимые разрешения: 16, 24, 32, 48, 64, 128, 255\n
    Примечание: * - необязательный пункт""")
        exit(1)

    image = Image.open(fp=filepath)

    try:
        icon_sizes = [(int(argv[2]), int(argv[2]))]
    except Exception:
        icon_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (255, 255)]

    for size in icon_sizes:
        image.save(fp=f"{filepath[:-4]}Icon{size[0]}.ico", sizes=[size], format="ico", quality=90)

    print("Конвертирование успешно выполнено!")


if __name__ == '__main__':
    main()
