# Последовательное-Параллельное выполнение
import asyncio

async def task(name, delay):
    print(f"{name} началась")
    await asyncio.sleep(delay)
    print(f"{name} завершилась через {delay} сек")

async def main():
    # Последовательное выполнение
    await task("Задача 1", 2)
    await task("Задача 2", 1)

    # Параллельное выполнение
    await asyncio.gather(
        task("Задача A", 3),
        task("Задача B", 2),
    )

asyncio.run(main())