import logging

from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from src.keyboards import main_menu, confirm_product, wishlist_kb, \
    confirm_delete_producs
from aiogram.types import FSInputFile, CallbackQuery
from db.users import add_user, save_product_and_link_user, get_wish_list, \
    delete_product_from_wishlist
from aiogram.fsm.context import FSMContext
from src.states import LinkInput
from parser.parser import parse_goldapple_product

logger = logging.getLogger(__name__)
main_router = Router()


@main_router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    text = (f"Золотое яблоко чеееек")

    photo = FSInputFile("src/images/main_menu.jpg")

    await message.answer_photo(
        photo=photo,
        caption=text,
        reply_markup=main_menu
    )
    tg_id = message.from_user.id
    username = message.from_user.username or f"id_{tg_id}"

    await add_user(tg_id, username)
    logger.info(f"{username} в главном меню")

@main_router.callback_query(F.data == "add_product")
async def handle_links_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("Отправьте ссылку, которую хотите сохранить:")
    await state.set_state(LinkInput.waiting_for_link)

@main_router.message(LinkInput.waiting_for_link)
async def handle_link_input(message: Message, state: FSMContext):
    user_link = message.text.strip()

    # Здесь можно сделать валидацию или сохранить ссылку
    await message.answer(f"Ссылка получена: {user_link}, получаю данные о товаре...")

    product_data = parse_goldapple_product(user_link)
    print(f"спарсили: {product_data}")

    await state.update_data(product_data=product_data, url=user_link)
    await state.set_state(LinkInput.waiting_for_confirmation)

    #ToDo удалить старое сообщение и добавить логирование
    await message.answer(
        f"<b>Найден товар:</b>\n"
        f"🏷 <b>Бренд:</b> {product_data.get('brand') or 'Нет данных'}\n"
        f"🔹 <b>Название:</b> {product_data.get('name') or 'Нет данных'}\n"
        f"💰 <b>Цена:</b> {product_data.get('price') or 'Нет данных'} ₽",
        parse_mode="HTML",
        reply_markup=confirm_product
    )

@main_router.callback_query(F.data.in_({"confirm_product", "cancel_product"}))
async def handle_confirmation(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if callback.data == "confirm_product":
        await save_product_and_link_user(
            tg_id=callback.from_user.id,
            product_data=data["product_data"],
            url=data["url"]
        )
        await callback.message.edit_text("✅ Товар успешно сохранён!")
    else:
        await callback.message.edit_text("❌ Сохранение отменено.")

    await state.clear()
    await start_handler(callback.message, state)


@main_router.callback_query(F.data == "wish_list")
async def handle_wishlist(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

    products = await get_wish_list(callback.from_user.id)

    if not products:
        text = "❌ У вас пока нет сохранённых товаров."
        return

    kb = wishlist_kb(products)

    await callback.message.answer(
        "<b>🛍 Ваша корзина </b>\nНажмите на товар, чтобы удалить:",
        reply_markup=kb,
        parse_mode="HTML"
    )

@main_router.callback_query(F.data.startswith("delete_"))
async def handle_delete_product(callback: CallbackQuery, state: FSMContext):
    product_id = int(callback.data.split("_")[1])

    await state.update_data(product_id_to_delete=product_id)

    await callback.message.answer(
        "❗️ Вы действительно хотите удалить товар из корзины?",
        reply_markup=confirm_delete_producs,
    )

@main_router.callback_query(F.data.in_({"confirm_delete", "cancel_delete"}))
async def confirm_delete_product(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if callback.data == "confirm_delete":
        product_id = data["product_id_to_delete"]

        await delete_product_from_wishlist(callback.from_user.id, product_id)
        await callback.message.delete()
        await callback.message.answer("✅ Товар успешно удалён из корзины.")
    else:
        await callback.message.answer("❌ Удаление товара отменено.")

    await state.clear()

    products = await get_wish_list(callback.from_user.id)

    await callback.message.answer(
        "🛍 Ваша корзина обновлена:",
        reply_markup=wishlist_kb(products)
    )
