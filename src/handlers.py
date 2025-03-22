import logging
import asyncio

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards import main_menu, instruction_menu, traps_menu, signal_menu, unregistered_menu, time_menu
from aiogram.types import FSInputFile

from utils import generate_random_values, reg_check, get_random_trend
from aiogram import Bot

logger = logging.getLogger(__name__)
main_router = Router()


@main_router.message(Command("start"))
async def start_handler(message: Message):
    text = (f"😎 Привет!\n"
            f"\n"
            f"🤖 Я - торговый робот, основанный на искусственном интеллекте ChatGPT 4.5, в связке с 15 индикаторами.\n"
            f"\n"
            f"🚨 Перед использованием, обязательно прочитай инструкцию.")

    photo = FSInputFile("images/main_menu.jpg")

    await message.answer_photo(
        photo=photo,
        caption=text,
        reply_markup=main_menu
    )
    username = message.from_user.username
    logger.info(f"{username} в главном меню")

@main_router.callback_query(lambda c: c.data == "btn2")
async def instruction_handler(callback: CallbackQuery):
    await callback.message.delete()

    text = (f"🤖 Бот основан и обучен на"
            f" миоклонической нейронной сети"
            f" OpenAI!"
            f"Для обучения бота было совершенно 30,000\n"
            f"сделок на маркете."
            f"В настоящее время пользователи бота"
            f"успешно генерируют 15-25% от своего"
            f"капитала ежедневно! 🎰\n"
            f"🟢 1. Создаем аккаунт PoketOption"
            f"(КНОПКА СНИЗУ)\n"
            f"❗️ Без регистрации доступ к сигналам не"
            f"будет открыт ❗️\n"
            f"🟢 2. Внести депозит от 5000Р.\n"
            f"🟢 3. Запросите сигнал у бота и ставьте"
            f"ставки в соответствии с сигналами от"
            f" бота.")

    await callback.message.answer(
        text,
        reply_markup=instruction_menu  # Отправляем новую клавиатуру
    )
    await callback.answer()  # Закрываем всплывающее уведомление
    username = callback.from_user.username
    logger.info(f"{username} читает инструкцию")

# Обработчик кнопки "Назад"
@main_router.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main_handler(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()

    await start_handler(callback.message)

# Обработчик кнопки "🚀 ВЫДАТЬ СИГНАЛ"
@main_router.callback_query(lambda c: c.data == "btn3")
async def send_signal_handler(callback: CallbackQuery):
    username = callback.from_user.username.lower()
    if not await reg_check(username, callback=callback):
        if callback.message and callback.message.message_id:
            try:
                await callback.message.delete()
            except Exception:
                pass  # Игнорируем ошибку, если сообщение уже удалено

        await callback.message.answer_photo(
            caption=(
            f"⚠️ Ошибка: Регистрация не пройдена!\n● Пройдите"
            f" регистрацию через главное меню, после завершения"
            f" регистрации, Вам автоматически откроется доступ к сигналам."),
            reply_markup=unregistered_menu,  # Переход на экран с новой клавиатурой
            photo=FSInputFile("images/unreg.jpg"),
        )
        logger.info(f"{username} байт на регистрацию")
    else:
        await callback.message.delete()  # Удаляем предыдущее сообщение
        logger.info(f"{username} выбирает торговую пару")
        text = "Выберите торговую пару 👇"
        await callback.message.answer(
            text,
            reply_markup=traps_menu  # Отправляем новую клавиатуру
        )
        await callback.answer()  # Закрываем всплывающее уведомление


@main_router.callback_query(lambda c: c.data.startswith("time_"))
async def traps_selected_handler(callback: CallbackQuery):
    await callback.message.delete()
    first_message = await callback.message.answer(
        "⏳ Подключение к серверу...\n(это может занять какое-то время)"
    )
    await asyncio.sleep(2)
    await first_message.delete()

    second_message = await callback.message.answer(
        "🌐 Соединение с сервером Binarium прошло успешно\n\n"
        "📊 Провожу анализ индикаторов и поиск устойчивого тренда по активу\n\n"
        "⏰ Примерное время ожидания ~15 секунд" # ЗДЕСЬ МЕНЯЕМ ЗАДЕРЖКУ ДО СИГНАЛА БОТА
    )
    await asyncio.sleep(2) # ЗДЕСЬ МЕНЯЕМ ЗАДЕРЖКУ ДО СИГНАЛА БОТА
    await second_message.delete()

    base_chance, max_chance, reversal_chance, volatility = generate_random_values()

    trend, smile = get_random_trend()

    final_message = (
        f"👁 Обнаружена линия тренда и проведен анализ связки индикаторов\n\n"
        f"📈 В выбранном временном отрезке график показывает тренд {trend}\n\n"
        f"✔️ Вероятность успешного входа: {base_chance} - {max_chance} %\n"
        f"🔄 Вероятность разворота: {reversal_chance} %\n"
        f"📊 Волатильность графика: {volatility}%\n\n"
        f"💡 Рекомендуется входить в сделку {trend}"
    )

    await callback.message.answer(final_message, reply_markup=signal_menu)

    logger.info(f"{callback.from_user.username} получил сигнал")


# Хендлер кнопки "🔄 Новый сигнал"
@main_router.callback_query(lambda c: c.data == "btn_new_signal")
async def new_signal_handler(callback: CallbackQuery):
    await traps_selected_handler(callback)  # Просто вызываем хендлер заново

# Хендлер выбранного времени эксприрации
@main_router.callback_query(lambda c: c.data.startswith("traps"))
async def time_selected_handler(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        text="Выберите время экспирации 👇",
        reply_markup=time_menu
    )
    await callback.answer()
    logger.info(f"{callback.from_user.username} выбирает время")