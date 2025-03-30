# src/services/price_checker.py
import asyncio
from parser.parser import parse_goldapple_product
from db.products import get_all_tracked_products, update_product_price, \
    get_user_by_product, increase_all_prices_by
from aiogram import Bot

CHECK_INTERVAL = 3600  # один час

async def check_prices_loop(bot: Bot):
    while True:
        print("[INFO] Запуск проверки цен...")
        await increase_all_prices_by(200.0)
        print("[DEBUG] Все цены увеличены на 200 руб.")
        products = await get_all_tracked_products()
        print(f"[DEBUG] Загружено {len(products)} товаров для проверки.")

        for product in products:
            url = product["url"]
            old_price = float(product["price"])
            new_data = parse_goldapple_product(url)
            new_price = float(new_data.get("price", 0))

            if new_price and new_price != old_price:
                await update_product_price(product["id"], new_price)

                if new_price < old_price:
                    # Уведомить пользователя
                    user = await get_user_by_product(product["id"])
                    if user:
                        text = (
                            f"💸 <b>Цена на отслеживаемый товар снизилась!</b>\n\n"
                            f"🏷 <b>Бренд:</b> {product['brand']}\n"
                            f"🔹 <b>Название:</b> {product['name']}\n"
                            f"📉 <b>Старая цена:</b> {old_price} ₽\n"
                            f"💰 <b>Новая цена:</b> {new_price} ₽\n"
                            f"🔗 <a href=\"{url}\">Ссылка на товар</a>"
                        )
                        print("Пытаюсь отправить инфу юзеру {user}")
                        await bot.send_message(user["tg_id"], text, parse_mode="HTML", disable_web_page_preview=True)

        await asyncio.sleep(CHECK_INTERVAL)
