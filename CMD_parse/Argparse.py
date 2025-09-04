import argparse

parser = argparse.ArgumentParser(description="Пример argparse")
parser.add_argument("--input", type=str, required=True, help="Входной файл")
parser.add_argument("--output", type=str, help="Выходной файл")
parser.add_argument("--verbose", action="store_true", help="Подробный вывод")

args = parser.parse_args()

if args.verbose:
    print(f"Обработка {args.input}...")
if args.output:
    print(f"Результат в {args.output}")