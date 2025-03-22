import os
import random


def get_random_signal_image() -> str:
    """
    Возвращает путь до случайной фотографии из папки images/signals.
    """
    folder_path = "images/signals"  # Папка с изображениями
    files = [f for f in os.listdir(folder_path) if f.lower().endswith((".png", ".jpg"))]

    if not files:
        raise FileNotFoundError("В папке images/signals нет изображений!")

    random_file = random.choice(files)  # Выбираем случайный файл
    return os.path.join(folder_path, random_file)  # Возвращаем полный путь

async def reg_check(user_name: str, callback):
    with open("users.txt", "r") as file:
        users = {line.strip() for line in file.readlines()}  # Читаем ID

    if user_name.lower() not in users:
        with open("users.txt", "a") as file:
            file.write(f"{user_name}\n")
            return False
    return True

def generate_random_values():
    """
    Генерирует случайные значения для вероятностей входа, разворота и волатильности.
    """
    base_chance = random.randint(82, 87)  # Генерируем число от 50 до 88
    max_chance = min(base_chance + 12, 100)  # Прибавляем 12%, но не выше 100%
    reversal_chance = random.randint(10, 50)  # Вероятность разворота от 20 до 50%
    volatility = random.randint(60, 100)  # Волатильность от 60 до 100
    return base_chance, max_chance, reversal_chance, volatility

def get_random_trend():
    """
    Рандомно выбирает тренд: ПОВЫШЕНИЕ (🟢) или СНИЖЕНИЕ (🔴).
    """
    if random.choice([True, False]):
        return "на 🟢 ПОВЫШЕНИЕ", "🟢"
    else:
        return "на 🔴 СНИЖЕНИЕ", "🔴"