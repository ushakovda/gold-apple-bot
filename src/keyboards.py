from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🛍 Моя корзина", callback_data="wish_list"),
         InlineKeyboardButton(text="📑 Инструкция", callback_data="asd")],
        [InlineKeyboardButton(text="🔎 Добавить товар ", callback_data="add_product", width=2)]
    ]
)

confirm_product = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Всё верно", callback_data="confirm_product"),
         InlineKeyboardButton(text="✖️ Отмена", callback_data="cancel_product")],
    ]
)

def wishlist_kb(products: list[dict]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f"{p['brand']} {p['name']} - {int(p['price'])}₽",
            callback_data=f"delete_{p['id']}"
        )] for p in products
    ])

confirm_delete_producs = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Да", callback_data="confirm_delete"),
                InlineKeyboardButton(text="✖️ Нет", callback_data="cancel_delete")
            ]
        ])